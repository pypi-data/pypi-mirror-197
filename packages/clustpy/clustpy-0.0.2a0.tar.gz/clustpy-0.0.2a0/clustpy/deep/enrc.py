"""
@authors:
Lukas Miklautz
"""

import torch
from sklearn.base import BaseEstimator, ClusterMixin
import numpy as np
from clustpy.deep._utils import int_to_one_hot, squared_euclidean_distance, encode_batchwise, detect_device, \
    set_torch_seed
from clustpy.deep._data_utils import get_dataloader
from clustpy.deep._train_utils import get_trained_autoencoder
from clustpy.alternative import NrKmeans
from sklearn.utils import check_random_state
from sklearn.metrics import normalized_mutual_info_score
from clustpy.utils.plots import plot_scatter_matrix
from clustpy.alternative.nrkmeans import _get_total_cost_function


class _ENRC_Module(torch.nn.Module):
    """
    The ENRC torch.nn.Module.

    Parameters
    ----------
    centers : list
        list containing the cluster centers for each clustering
    P : list
        list containing projections for each clustering
    V : np.ndarray
        orthogonal rotation matrix
    beta_init_value : float
        initial values of beta weights. Is ignored if beta_weights is not None (default: 0.9)
    degree_of_space_distortion : float
        weight of the cluster loss term. The higher it is set the more the embedded space will be shaped to the assumed cluster structure (default: 1.0)
    degree_of_space_preservation : float
        weight of regularization loss term, e.g., reconstruction loss (default: 1.0)
    center_lr : float
        weight for updating the centers via mini-batch k-means. Has to be set between 0 and 1. If set to 1.0 than only the mini-batch centroid will be used,
        neglecting the past state and if set to 0 then no update is happening (default: 0.5)
    rotate_centers : bool
        if True then centers are multiplied with V before they are used, because ENRC assumes that the centers lie already in the V-rotated space (default: False)
    beta_weights : np.ndarray
        initial beta weights for the softmax (optional). If not None, then beta_init_value will be ignored (default: None)

    Attributes
    ----------
    lonely_centers_count : list
        list of np.ndarrays, count indicating how often a center in a clustering has not received any updates, because no points were assigned to it.
        The lonely_centers_count of a center is reset if it has been reinitialized.
    mask_sum : list
        list of torch.tensors, contains the average number of points assigned to each cluster in each clustering over the training.
    reinit_threshold : int
        threshold that indicates when a cluster should be reinitialized. Starts with 1 and increases during training with int(np.sqrt(i+1)), where i is the number of mini-batch iterations.

    Raises
    ----------
    ValueError : if center_lr is not in [0,1]
    """

    def __init__(self, centers: list, P: list, V: np.ndarray, beta_init_value: float = 0.9,
                 degree_of_space_distortion: float = 1.0, degree_of_space_preservation: float = 1.0,
                 center_lr: float = 0.5, rotate_centers: bool = False, beta_weights: np.ndarray = None):
        super().__init__()

        self.P = P
        self.m = [len(P_i) for P_i in self.P]
        if beta_weights is None:
            beta_weights = beta_weights_init(self.P, n_dims=centers[0].shape[1], high_value=beta_init_value)
        else:
            beta_weights = torch.tensor(beta_weights).float()
        self.beta_weights = torch.nn.Parameter(beta_weights, requires_grad=True)
        self.V = torch.nn.Parameter(torch.tensor(V, dtype=torch.float), requires_grad=True)
        self.degree_of_space_distortion = degree_of_space_distortion
        self.degree_of_space_preservation = degree_of_space_preservation

        # Center specific initializations
        if rotate_centers:
            centers = [np.matmul(centers_sub, V) for centers_sub in centers]
        self.centers = [torch.tensor(centers_sub, dtype=torch.float32) for centers_sub in centers]
        if not (0 <= center_lr <= 1):
            raise ValueError(f"center_lr={center_lr}, but has to be in [0,1].")
        self.center_lr = center_lr
        self.lonely_centers_count = []
        self.mask_sum = []
        for centers_i in self.centers:
            self.lonely_centers_count.append(np.zeros((centers_i.shape[0], 1)).astype(int))
            self.mask_sum.append(torch.zeros((centers_i.shape[0], 1)))
        self.reinit_threshold = 1

    def to_device(self, device: torch.device) -> '_ENRC_Module':
        """
        Loads all ENRC parameters to device that are needed during the training and prediction (including the learnable parameters).
        This function is preferred over the to(device) function.

        Parameters
        ----------
        device : torch.device
            device to be trained on

        Returns
        -------
        self : _ENRC_Module
            this instance of the ENRC_Module
        """
        self.to(device)
        self.centers = [c_i.to(device) for c_i in self.centers]
        self.mask_sum = [i.to(device) for i in self.mask_sum]
        return self

    def subspace_betas(self) -> torch.Tensor:
        """
        Returns a len(P) x d matrix with softmax weights, where d is the number of dimensions of the embedded space, indicating
        which dimensions belongs to which clustering.

        Returns
        -------
        self : torch.Tensor
            the dimension assignments
        """
        dimension_assignments = torch.nn.functional.softmax(self.beta_weights, dim=0)
        return dimension_assignments

    def get_P(self) -> list:
        """
        Converts the soft beta weights back to hard assignments P and returns them as a list.

        Returns
        -------
        P : list
            list containing indices for projections for each clustering
        """
        P = _get_P(betas=self.subspace_betas().detach().cpu(), centers=self.centers)
        return P

    def rotate(self, z: torch.Tensor) -> torch.Tensor:
        """
        Rotate the embedded data ponint z using the orthogonal rotation matrix V.

        Parameters
        ----------
        z : torch.Tensor
            embedded data point, can also be a mini-batch of points

        Returns
        -------
        z_rot : torch.Tensor
            the rotated embedded data point
        """
        z_rot = _rotate(z, self.V)
        return z_rot

    def rotate_back(self, z_rot: torch.Tensor) -> torch.Tensor:
        """
        Rotate a rotated embedded data point back to its original state.

        Parameters
        ----------
        z_rot : torch.Tensor
            rotated and embedded data point, can also be a mini-batch of points

        Returns
        -------
        z : torch.Tensor
            the back-rotated embedded data point
        """
        z = _rotate_back(z_rot, self.V)
        return z

    def rotation_loss(self) -> torch.Tensor:
        """
        Computes how much the rotation matrix self.V diverges from an orthogonal matrix by calculating |V^T V - I|.
        For an orthogonal matrix this difference is 0, as V^T V=I.

        Returns
        -------
        rotation_loss : torch.Tensor
            the average absolute difference between V^T times V - the identity matrix I.
        """
        ident = torch.matmul(self.V.t(), self.V).detach().cpu()
        rotation_loss = (ident - torch.eye(n=ident.shape[0])).abs().mean()
        return rotation_loss

    def update_center(self, data: torch.Tensor, one_hot_mask: torch.Tensor, subspace_id: int) -> None:
        """
        Inplace update of centers of a clusterings in subspace=subspace_id in a mini-batch fashion.

        Parameters
        ----------
        data : torch.Tensor
            data points, can also be a mini-batch of points
        one_hot_mask : torch.Tensor
            one hot encoded matrix of cluster assignments
        subspace_id : int
            integer which indicates which subspace the cluster to be updated are in

        Raises
        ----------
        ValueError: If None values are encountered.
        """
        if self.centers[subspace_id].shape[0] == 1:
            # Shared space update with only one cluster
            self.centers[subspace_id] = self.centers[subspace_id] * 0.5 + data.mean(0).unsqueeze(0) * 0.5
        else:

            batch_cluster_sums = (data.unsqueeze(1) * one_hot_mask.unsqueeze(2)).sum(0)
            mask_sum = one_hot_mask.sum(0).unsqueeze(1)
            if (mask_sum == 0).sum().int().item() != 0:
                idx = (mask_sum == 0).nonzero()[:, 0].detach().cpu()
                self.lonely_centers_count[subspace_id][idx] += 1

            # In case mask sum is zero batch cluster sum is also zero so we can add a small constant to mask sum and center_lr
            # Avoid division by a small number
            mask_sum += 1e-8
            # Use weighted average
            nonzero_mask = (mask_sum.squeeze(1) != 0)
            self.mask_sum[subspace_id][nonzero_mask] = self.center_lr * mask_sum[nonzero_mask] + (1 - self.center_lr) * \
                                                       self.mask_sum[subspace_id][nonzero_mask]

            per_center_lr = 1.0 / (1 + self.mask_sum[subspace_id][nonzero_mask])
            self.centers[subspace_id] = (1.0 - per_center_lr) * self.centers[subspace_id][
                nonzero_mask] + per_center_lr * batch_cluster_sums[nonzero_mask] / mask_sum[nonzero_mask]
            if torch.isnan(self.centers[subspace_id]).sum() > 0:
                raise ValueError(
                    f"Found nan values\n self.centers[subspace_id]: {self.centers[subspace_id]}\n per_center_lr: {per_center_lr}\n self.mask_sum[subspace_id]: {self.mask_sum[subspace_id]}\n ")

    def update_centers(self, z_rot: torch.Tensor, assignment_matrix_dict: dict) -> None:
        """
        Inplace update of all centers in all clusterings in a mini-batch fashion.

        Parameters
        ----------
        z_rot : torch.Tensor
            rotated data point, can also be a mini-batch of points
        assignment_matrix_dict : dict
            dict of torch.tensors, contains for each i^th clustering a one hot encoded matrix of cluster assignments
        """
        for subspace_i in range(len(self.centers)):
            self.update_center(z_rot.detach(),
                               assignment_matrix_dict[subspace_i],
                               subspace_id=subspace_i)

    def forward(self, z: torch.Tensor) -> (torch.Tensor, torch.Tensor, torch.Tensor, dict):
        """
        Calculates the k-means loss and cluster assignments for each clustering.

        Parameters
        ----------
        z : torch.Tensor
            embedded input data point, can also be a mini-batch of embedded points

        Returns
        -------
        tuple : (torch.Tensor, torch.Tensor, torch.Tensor, dict)
            averaged sum of all k-means losses for each clustering,
            the rotated embedded point,
            the back rotated embedded point,
            dict of torch.tensors, contains for each i^th clustering a one hot encoded matrix of cluster assignments
        """
        z_rot = self.rotate(z)
        z_rot_back = self.rotate_back(z_rot)

        subspace_betas = self.subspace_betas()
        subspace_losses = 0
        assignment_matrix_dict = {}
        for i, centers_i in enumerate(self.centers):
            weighted_squared_diff = squared_euclidean_distance(z_rot, centers_i.detach(), weights=subspace_betas[i, :])
            weighted_squared_diff /= z_rot.shape[0]
            assignments = weighted_squared_diff.detach().argmin(1)
            one_hot_mask = int_to_one_hot(assignments, centers_i.shape[0])
            weighted_squared_diff_masked = weighted_squared_diff * one_hot_mask
            subspace_losses += weighted_squared_diff_masked.sum()
            assignment_matrix_dict[i] = one_hot_mask
        subspace_losses = subspace_losses / subspace_betas.shape[0]
        return subspace_losses, z_rot, z_rot_back, assignment_matrix_dict

    def predict(self, z: torch.Tensor, use_P: bool = False) -> np.ndarray:
        """
        Predicts the labels for each clustering of an input z.

        Parameters
        ----------
        z : torch.Tensor
            embedded input data point, can also be a mini-batch of embedded points
        use_P: bool
            if True then P will be used to hard select the dimensions for each clustering, else the soft beta weights are used (default: False)

        Returns
        -------
        predicted_labels : np.ndarray
            n x c matrix, where n is the number of data points in z and c is the number of clusterings.
        """
        predicted_labels = enrc_predict(z=z, V=self.V, centers=self.centers, subspace_betas=self.subspace_betas(),
                                        use_P=use_P)
        return predicted_labels

    def predict_batchwise(self, model: torch.nn.Module, dataloader: torch.utils.data.DataLoader,
                          device: torch.device = torch.device("cpu"), use_P: bool = False) -> np.ndarray:
        """
        Predicts the labels for each clustering of a dataloader in a mini-batch manner.

        Parameters
        ----------
        model : torch.nn.Module
            the input model for encoding the data
        dataloader : torch.utils.data.DataLoader
            dataloader to be used for prediction
        device : torch.device
            device to be predicted on (default: torch.device('cpu'))
        use_P: bool
            if True then P will be used to hard select the dimensions for each clustering, else the soft beta weights are used (default: False)

        Returns
        -------
        predicted_labels : np.ndarray
            n x c matrix, where n is the number of data points in z and c is the number of clusterings.
        """
        predicted_labels = enrc_predict_batchwise(V=self.V, centers=self.centers, model=model, dataloader=dataloader,
                                                  subspace_betas=self.subspace_betas(), device=device, use_P=use_P)
        return predicted_labels

    def recluster(self, dataloader: torch.utils.data.DataLoader, model: torch.nn.Module,
                  device: torch.device = torch.device('cpu'), rounds: int = 1) -> None:
        """
        Recluster ENRC inplace using NrKMeans or SGD (depending on the data set size, see init='auto' for details).
        Can lead to improved and more stable performance.
        Updates self.P, self.beta_weights, self.V and self.centers.

        Parameters
        ----------
        dataloader : torch.utils.data.DataLoader
            dataloader to be used for prediction
        model : torch.nn.Module
            the input model for encoding the data
        device : torch.device
            device to be predicted on (default: torch.device('cpu'))
        rounds : int
            number of repetitions of the reclustering procedure (default: 1)
        """

        # Extract parameters
        V = self.V.detach().cpu().numpy()
        n_clusters = [c.shape[0] for c in self.centers]

        # Encode data
        embedded_data = encode_batchwise(dataloader, model, device)
        embedded_rot = np.matmul(embedded_data, V)

        # Apply reclustering in the rotated space, because V does not have to be orthogonal, so it could learn a mapping that is not recoverable by nrkmeans.
        centers_reclustered, P, new_V, beta_weights = enrc_init(data=embedded_rot, n_clusters=n_clusters, rounds=rounds,
                                                                max_iter=300, learning_rate=self.learning_rate,
                                                                init="auto", debug=False)

        # Update V, because we applied the reclustering in the rotated space
        new_V = np.matmul(V, new_V)

        # Assign reclustered parameters
        self.P = P
        self.m = [len(P_i) for P_i in self.P]
        self.beta_weights = torch.nn.Parameter(torch.from_numpy(beta_weights).float(), requires_grad=True)
        self.V = torch.nn.Parameter(torch.tensor(new_V, dtype=torch.float), requires_grad=True)
        self.centers = [torch.tensor(centers_sub, dtype=torch.float32) for centers_sub in centers_reclustered]
        self.to_device(device)

    def fit(self, data: torch.Tensor, optimizer: torch.optim.Optimizer, max_epochs: int, model: torch.nn.Module,
            batch_size: int, loss_fn: torch.nn.modules.loss._Loss = torch.nn.MSELoss(),
            device: torch.device = torch.device("cpu"), print_step: int = 10, debug: bool = True,
            scheduler: torch.optim.lr_scheduler = None, fix_rec_error: bool = False,
            tolerance_threshold: float = None) -> (torch.nn.Module, '_ENRC_Module'):
        """
        Trains ENRC and the autoencoder in place.

        Parameters
        ----------
        data : torch.Tensor / np.ndarray
            dataset to be used for training
        optimizer : torch.optim.Optimizer
            parameterized optimizer to be used
        max_epochs : int
            maximum number of epochs for training
        model : torch.nn.Module
            The underlying autoencoder
        batch_size: int
            batch size for dataloader
        loss_fn : torch.nn.modules.loss._Loss
            loss function to be used for reconstruction (default: torch.nn.MSELoss())
        device : torch.device
            device to be trained on (default: torch.device('cpu'))
        print_step : int
            specifies how often the losses are printed (default: 10)
        debug : bool
            if True than training errors will be printed (default: True)
        scheduler : torch.optim.lr_scheduler
            parameterized learning rate scheduler that should be used (default: None)
        fix_rec_error : bool
            if set to True than reconstruction loss is weighted proportionally to the cluster loss. Only used for init='sgd' (default: False)
        tolerance_threshold : float
            tolerance threshold to determine when the training should stop. If the NMI(old_labels, new_labels) >= (1-tolerance_threshold)
            for all clusterings then the training will stop before max_epochs is reached. If set high than training will stop earlier then max_epochs, and if set to 0 or None the training
            will train as long as the labels are not changing anymore (default: None)

        Returns
        -------
        tuple : (torch.nn.Module, _ENRC_Module)
            trained autoencoder,
            trained enrc module
        """
        # Deactivate Batchnorm and dropout
        model.eval()
        model.to(device)
        self.to_device(device)

        # Save learning rate for reclustering
        self.learning_rate = optimizer.param_groups[0]["lr"]
        # Evalloader is used for checking label change. Only difference to the trainloader here is that shuffle=False.
        trainloader = get_dataloader(data, batch_size=batch_size, shuffle=True, drop_last=True)
        evalloader = get_dataloader(data, batch_size=batch_size, shuffle=False, drop_last=False)

        i = 0
        labels_old = None
        for epoch_i in range(max_epochs):
            for batch in trainloader:
                batch = batch[1].to(device)

                z = model.encode(batch)
                subspace_loss, z_rot, z_rot_back, assignment_matrix_dict = self(z)
                reconstruction = model.decode(z_rot_back)
                rec_loss = loss_fn(reconstruction, batch)

                if fix_rec_error:
                    rec_weight = subspace_loss.item() / (rec_loss.item() + 1e-3)
                    if rec_weight < 1:
                        rec_weight = 1.0
                    rec_loss *= rec_weight

                summed_loss = self.degree_of_space_distortion * subspace_loss + self.degree_of_space_preservation * rec_loss
                optimizer.zero_grad()
                summed_loss.backward()
                optimizer.step()

                # Update Assignments and Centroids on GPU
                with torch.no_grad():
                    self.update_centers(z_rot, assignment_matrix_dict)
                # Check if clusters have to be reinitialized
                for subspace_i in range(len(self.centers)):
                    reinit_centers(enrc=self, subspace_id=subspace_i, dataloader=trainloader, model=model,
                                   n_samples=512, kmeans_steps=10)

                # Increase reinit_threshold over time
                self.reinit_threshold = int(np.sqrt(i + 1))

                i += 1
            if (epoch_i - 1) % print_step == 0 or epoch_i == (max_epochs - 1):
                with torch.no_grad():
                    # Rotation loss is calculated to check if its deviation from an orthogonal matrix
                    rotation_loss = self.rotation_loss()
                    if debug:
                        print(
                            f"Epoch {epoch_i}/{max_epochs - 1}: summed_loss: {summed_loss.item():.4f}, subspace_losses: {subspace_loss.item():.4f}, rec_loss: {rec_loss.item():.4f}, rotation_loss: {rotation_loss.item():.4f}")

            if scheduler is not None:
                scheduler.step()

            # Check if labels have changed
            labels_new = self.predict_batchwise(model=model, dataloader=evalloader, device=device, use_P=True)
            if _are_labels_equal(labels_new=labels_new, labels_old=labels_old, threshold=tolerance_threshold):
                # training has converged
                if debug:
                    print("Clustering has converged")
                break
            else:
                labels_old = labels_new.copy()

        # Extract P and m
        self.P = self.get_P()
        self.m = [len(P_i) for P_i in self.P]
        return model, self


"""
===================== Helper Functions =====================
"""


class _IdentityAutoencoder(torch.nn.Module):
    """
    Convenience class to avoid reimplementation of the remaining ENRC pipeline for the initialization.
    Encoder and decoder are here just identity functions implemented via lambda x:x.

    Attributes
    ----------
    encoder : function
        the encoder part
    decoder : function
        the decoder part
    """

    def __init__(self):
        super(_IdentityAutoencoder, self).__init__()

        self.encoder = lambda x: x
        self.decoder = lambda x: x

    def encode(self, x: torch.Tensor) -> torch.Tensor:
        """
        Apply the encoder function to x.

        Parameters
        ----------
        x : torch.Tensor
            input data point, can also be a mini-batch of points

        Returns
        -------
        encoded : torch.Tensor
            the encoeded data point
        """
        return self.encoder(x)

    def decode(self, embedded: torch.Tensor) -> torch.Tensor:
        """
        Apply the decoder function to embedded.

        Parameters
        ----------
        embedded : torch.Tensor
            embedded data point, can also be a mini-batch of embedded points

        Returns
        -------
        decoded : torch.Tensor
            returns the reconstruction of embedded
        """
        return self.decoder(embedded)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Applies both the encode and decode function.
        The forward function is automatically called if we call self(x).

        Parameters
        ----------
        x : torch.Tensor
            input data point, can also be a mini-batch of embedded points

        Returns
        -------
        reconstruction : torch.Tensor
            returns the reconstruction of a data point
        """
        embedded = self.encode(x)
        reconstruction = self.decode(embedded)
        return reconstruction


def _get_P(betas: torch.Tensor, centers: list, shared_space_variation: float = 0.05) -> float:
    """
    Converts the softmax betas back to hard assignments P and returns them as a list.

    Parameters
    ----------
    betas : torch.Tensor
        c x d soft assignment weights matrix for c clusterings and d dimensions.
    centers : list
        list of torch.Tensor, cluster centers for each clustering
    shared_space_variation : float
        specifies how much beta in the shared space is allowed to diverge from the uniform distribution. Only needed if a shared space (space with one cluster) exists (default: 0.05)

    Returns
    ----------
    P : list
        list containing indices for projections for each clustering
    """
    # Check if a shared space with a single cluster center exist
    shared_space_idx = [i for i, centers_i in enumerate(centers) if centers_i.shape[0] == 1]
    if shared_space_idx:
        # Specifies how much beta in the shared space is allowed to diverge from the uniform distribution
        shared_space_idx = shared_space_idx[0]
        equal_threshold = 1.0 / betas.shape[0]
        # Increase Weight of shared space dimensions that are close to the uniform distribution
        equal_threshold -= shared_space_variation
        betas[shared_space_idx][betas[shared_space_idx] > equal_threshold] += 1

    # Select highest assigned dimensions to P
    max_assigned_dims = betas.argmax(0)
    P = [[] for _ in range(betas.shape[0])]
    for dim_i, cluster_subspace_id in enumerate(max_assigned_dims):
        P[cluster_subspace_id].append(dim_i)
    return P


def _rotate(z: torch.Tensor, V: torch.Tensor) -> torch.Tensor:
    """
    Rotate the embedded data ponint z using the orthogonal rotation matrix V.

    Parameters
    ----------
    V : torch.Tensor
        orthogonal rotation matrix
    z : torch.Tensor
        embedded data point, can also be a mini-batch of points
    
    Returns
    -------
    z_rot : torch.Tensor
        the rotated embedded data point
    """
    return torch.matmul(z, V)


def _rotate_back(z_rot: torch.Tensor, V: torch.Tensor) -> torch.Tensor:
    """
    Rotate a rotated embedded data point back to its original state.

    Parameters
    ----------
    z_rot : torch.Tensor
        rotated and embedded data point, can also be a mini-batch of points
    V : torch.Tensor
        orthogonal rotation matrix
    
    Returns
    -------
    z : torch.Tensor
        the back-rotated embedded data point
    """
    return torch.matmul(z_rot, V.t())


def enrc_predict(z: torch.Tensor, V: torch.Tensor, centers: list, subspace_betas: torch.Tensor,
                 use_P: bool = False) -> np.ndarray:
    """
    Predicts the labels for each clustering of an input z.

    Parameters
    ----------
    z : torch.Tensor
        embedded input data point, can also be a mini-batch of embedded points
    V : torch.tensor
        orthogonal rotation matrix
    centers : list
        list of torch.Tensor, cluster centers for each clustering
    subspace_betas : torch.Tensor
        weights for each dimension per clustering. Calculated via softmax(beta_weights).
    use_P: bool
        if True then P will be used to hard select the dimensions for each clustering, else the soft subspace_beta weights are used (default: False)

    Returns
    -------
    predicted_labels : np.ndarray
        n x c matrix, where n is the number of data points in z and c is the number of clusterings.
    """
    z_rot = _rotate(z, V)
    if use_P:
        P = _get_P(betas=subspace_betas.detach(), centers=centers)
    labels = []
    for i, centers_i in enumerate(centers):
        if use_P:
            weighted_squared_diff = squared_euclidean_distance(z_rot[:, P[i]], centers_i[:, P[i]])
        else:
            weighted_squared_diff = squared_euclidean_distance(z_rot, centers_i, weights=subspace_betas[i, :])
        labels_sub = weighted_squared_diff.argmin(1)
        labels_sub = labels_sub.detach().cpu().numpy().astype(np.int32)
        labels.append(labels_sub)
    return np.stack(labels).transpose()


def enrc_predict_batchwise(V: torch.Tensor, centers: list, subspace_betas: torch.Tensor, model: torch.nn.Module,
                           dataloader: torch.utils.data.DataLoader, device: torch.device = torch.device("cpu"),
                           use_P: bool = False) -> np.ndarray:
    """
    Predicts the labels for each clustering of a dataloader in a mini-batch manner.

    Parameters
    ----------
    V : torch.Tensor
        orthogonal rotation matrix
    centers : list
        list of torch.Tensor, cluster centers for each clustering
    subspace_betas : torch.Tensor
        weights for each dimension per clustering. Calculated via softmax(beta_weights).
    model : torch.nn.Module
        the input model for encoding the data
    dataloader : torch.utils.data.DataLoader
        dataloader to be used for prediction
    device : torch.device
        device to be predicted on (default: torch.device('cpu'))
    use_P: bool
        if True then P will be used to hard select the dimensions for each clustering, else the soft beta weights are used (default: False)
    
    Returns
    -------
    predicted_labels : np.ndarray
        n x c matrix, where n is the number of data points in z and c is the number of clusterings.
    """
    model.eval()
    predictions = []
    with torch.no_grad():
        for batch in dataloader:
            batch_data = batch[1].to(device)
            z = model.encode(batch_data)
            pred_i = enrc_predict(z=z, V=V, centers=centers, subspace_betas=subspace_betas, use_P=use_P)
            predictions.append(pred_i)
    return np.concatenate(predictions)


"""
===================== Initialization Strategies =====================
"""


def available_init_strategies() -> list:
    """
    Returns a list of strings of available initialization strategies for ENRC.
    At the moment following strategies are supported: nrkmeans, random, sgd, auto
    """
    return ['nrkmeans', 'random', 'sgd', 'auto']


def optimal_beta(kmeans_loss: torch.Tensor, other_losses_mean_sum: torch.Tensor) -> torch.Tensor:
    """
    Calculate optimal values for the beta weight for each dimension.
    
    Parameters
    ----------
    kmeans_loss: torch.Tensor
        a 1 x d vector of the kmeans losses per dimension.
    other_losses_mean_sum: torch.Tensor
        a 1 x d vector of the kmeans losses of all other clusterings except the one in 'kmeans_loss'.
    
    Returns
    -------
    optimal_beta_weights: torch.Tensor
        a 1 x d vector containing the optimal weights for the softmax to indicate which dimensions are important for each clustering.
        Calculated via -torch.log(kmeans_loss/other_losses_mean_sum)
    """
    return -torch.log(kmeans_loss / other_losses_mean_sum)


def calculate_optimal_beta_weights_special_case(data: torch.Tensor, centers: list, V: torch.Tensor,
                                                batch_size: int = 32) -> torch.Tensor:
    """
    The beta weights have a closed form solution if we have two subspaces, so the optimal values given the data, centers and V can be computed.
    See supplement of Lukas Miklautz, Lena G. M. Bauer, Dominik Mautz, Sebastian Tschiatschek, Christian Boehm, Claudia Plant: Details (Don't) Matter: Isolating Cluster Information in Deep Embedded Spaces. IJCAI 2021: 2826-2832
    here: https://gitlab.cs.univie.ac.at/lukas/acedec_public/-/blob/master/supplement.pdf

    Parameters
    ----------
    data : torch.Tensor
        input data
    centers : list
        list of torch.Tensor, cluster centers for each clustering
    V : torch.Tensor
        orthogonal rotation matrix
    batch_size : int
        size of the data batches (default: 32)

    Returns
    -------
    optimal_beta_weights: torch.Tensor
        a c x d vector containing the optimal weights for the softmax to indicate which dimensions d are important for each clustering c.
    """
    dataloader = get_dataloader(data, batch_size=batch_size, shuffle=True, drop_last=False)
    device = V.device
    with torch.no_grad():
        # calculate kmeans losses for each clustering
        km_losses = [[] for _ in centers]
        for batch in dataloader:
            batch = batch[1].to(device)
            z_rot = torch.matmul(batch, V)
            for i, centers_i in enumerate(centers):
                weighted_squared_diff = squared_euclidean_distance(z_rot.unsqueeze(1), centers_i.unsqueeze(1))
                assignments = weighted_squared_diff.detach().sum(2).argmin(1)
                one_hot_mask = int_to_one_hot(assignments, centers_i.shape[0])
                weighted_squared_diff_masked = weighted_squared_diff * one_hot_mask.unsqueeze(2)
                km_losses[i].append(weighted_squared_diff_masked.detach().cpu())

        for i, km_loss in enumerate(km_losses):
            # Sum over samples and centers
            km_losses[i] = torch.cat(km_loss, 0).mean(0).mean(0)

        # calculate beta_weights for each dimension and clustering based on kmeans losses
        best_weights = []
        best_weights.append(optimal_beta(km_losses[0], km_losses[1]))
        best_weights.append(optimal_beta(km_losses[1], km_losses[0]))
        best_weights = torch.stack(best_weights)
    return best_weights


def beta_weights_init(P: list, n_dims: int, high_value: float = 0.9) -> torch.Tensor:
    """
    Initializes parameters of the softmax such that betas will be set to high_value in dimensions which form a cluster subspace according to P
    and set to (1 - high_value)/(len(P) - 1) for the other clusterings.
    
    Parameters
    ----------
    P : list
        list containing projections for each subspace
    n_dims : int
        dimensionality of the embedded data
    high_value : float
        value that should be initially used to indicate strength of assignment of a specific dimension to the clustering (default: 0.9)
    
    Returns
    ----------
    beta_weights : torch.Tensor
        initialized weights that are input in the softmax to get the betas.
    """
    weight_high = 1.0
    n_sub_clusterings = len(P)
    beta_hard = np.zeros((n_sub_clusterings, n_dims), dtype=np.float32)
    for sub_i, p in enumerate(P):
        for dim in p:
            beta_hard[sub_i, dim] = 1.0
    low_value = 1.0 - high_value
    weight_high_exp = np.exp(weight_high)
    # Because high_value = weight_high/(weight_high +low_classes*weight_low)
    n_low_classes = len(P) - 1
    weight_low_exp = weight_high_exp * (1.0 - high_value) / (high_value * n_low_classes)
    weight_low = np.log(weight_low_exp)
    beta_soft_weights = beta_hard * (weight_high - weight_low) + weight_low
    return torch.tensor(beta_soft_weights, dtype=torch.float32)


def calculate_beta_weight(data: torch.Tensor, centers: list, V: torch.Tensor, P: list,
                          high_beta_value: float = 0.9) -> torch.Tensor:
    """
    The beta weights have a closed form solution if we have two subspaces, so the optimal values given the data, centers and V can be computed.
    See supplement of Lukas Miklautz, Lena G. M. Bauer, Dominik Mautz, Sebastian Tschiatschek, Christian Boehm, Claudia Plant: Details (Don't) Matter: Isolating Cluster Information in Deep Embedded Spaces. IJCAI 2021: 2826-2832
    here: https://gitlab.cs.univie.ac.at/lukas/acedec_public/-/blob/master/supplement.pdf
    For number of subspaces > 2, we calculate the beta weight assuming that an assigned subspace should have a weight of 0.9.
    
    Parameters
    ----------
    data : torch.Tensor
        input data
    centers : list
        list of torch.Tensor, cluster centers for each clustering
    V : torch.Tensor
        orthogonal rotation matrix
    P : list
        list containing projections for each subspace
    high_beta_value : float
        value that should be initially used to indicate strength of assignment of a specific dimension to the clustering (default: 0.9)

    Returns
    -------
    beta_weights: torch.Tensor
        a c x d vector containing the weights for the softmax to indicate which dimensions d are important for each clustering c.

    Raises
    -------
    ValueError: If number of clusterings is smaller than 2
    """
    n_clusterings = len(centers)
    if n_clusterings == 2:
        beta_weights = calculate_optimal_beta_weights_special_case(data=data, centers=centers, V=V)
    elif n_clusterings > 2:
        beta_weights = beta_weights_init(P=P, n_dims=data.shape[1], high_value=high_beta_value)

    else:
        raise ValueError(f"Number of clusterings is {n_clusterings}, but should be >= 2")
    return beta_weights


def nrkmeans_init(data: np.ndarray, n_clusters: list, rounds: int = 10, max_iter: int = 100, input_centers: list = None,
                  P: list = None, V: np.ndarray = None, random_state: np.random.RandomState = None, debug=True) -> (
        list, list, np.ndarray, np.ndarray):
    """
    Initialization strategy based on the NrKmeans Algorithm. This strategy is preferred for small data sets, but the orthogonality
    constraint on V and subsequently for the clustered subspaces can be sometimes to limiting in practice, e.g., if clusterings are
    not perfectly non-redundant.

    Parameters
    ----------
    data : np.ndarray
        input data
    n_clusters : list
        list of ints, number of clusters for each clustering
    rounds : int
        number of repetitions of the NrKmeans algorithm (default: 10)
    max_iter : int
        maximum number of iterations of NrKmeans (default: 100)
    input_centers : list
        list of np.ndarray, optional parameter if initial cluster centers want to be set (optional) (default: None)
    P : list
        list containing projections for each subspace (optional) (default: None)
    V : np.ndarray
        orthogonal rotation matrix (optional) (default: None)
    random_state : np.random.RandomState
        use a fixed random state to get a repeatable solution. Can also be of type int (default: None)
    debug : bool
        if True then the cost of each round will be printed (default: True)

    Returns
    -------
    tuple : (list, list, np.ndarray, np.ndarray)
        list of cluster centers for each subspace
        list containing projections for each subspace
        orthogonal rotation matrix
        weights for softmax function to get beta values.
    """
    best = None
    lowest = np.inf
    for i in range(rounds):
        nrkmeans = NrKmeans(n_clusters=n_clusters, cluster_centers=input_centers, P=P, V=V, max_iter=max_iter,
                            random_state=random_state)
        nrkmeans.fit(X=data)
        centers_i, P_i, V_i, scatter_matrices_i = nrkmeans.cluster_centers, nrkmeans.P, nrkmeans.V, nrkmeans.scatter_matrices_
        if len(P_i) != len(n_clusters):
            if debug:
                print(
                    f"WARNING: Lost Subspace. Found only {len(P_i)} subspaces for {len(n_clusters)} clusterings. Try to increase the size of the embedded space or the number of iterations of nrkmeans to avoid this from happening.")
        else:
            cost = _get_total_cost_function(V=V_i, P=P_i, scatter_matrices=scatter_matrices_i)
            if lowest > cost:
                best = [centers_i, P_i, V_i, ]
                lowest = cost
            if debug:
                print(f"Round {i}: Found solution with: {cost} (current best: {lowest})")
    # Best parameters
    centers, P, V = best
    # centers are expected to be rotated for ENRC
    centers = [np.matmul(centers_sub, V) for centers_sub in centers]
    beta_weights = calculate_beta_weight(data=torch.from_numpy(data).float(),
                                         centers=[torch.from_numpy(centers_sub).float() for centers_sub in centers],
                                         V=torch.from_numpy(V).float(),
                                         P=P)
    beta_weights = beta_weights.detach().cpu().numpy()

    return centers, P, V, beta_weights


def random_nrkmeans_init(data: np.ndarray, n_clusters: list, rounds: int = 10, input_centers: list = None,
                         P: list = None, V: np.ndarray = None, random_state: np.random.RandomState = None,
                         debug: bool = True) -> (list, list, np.ndarray, np.ndarray):
    """
    Initialization strategy based on the NrKmeans Algorithm. For documentation see nrkmeans_init function.
    Same as nrkmeans_init, but max_iter is set to 5, so the results will be faster and more random.

    Parameters
    ----------
    data : np.ndarray
        input data
    n_clusters : list
        list of ints, number of clusters for each clustering
    rounds : int
        number of repetitions of the NrKmeans algorithm (default: 10)
    input_centers : list
        list of np.ndarray, optional parameter if initial cluster centers want to be set (optional) (default: None)
    P : list
        list containing projections for each subspace (optional) (default: None)
    V : np.ndarray
        orthogonal rotation matrix (optional) (default: None)
    random_state : np.random.RandomState
        use a fixed random state to get a repeatable solution. Can also be of type int (default: None)
    debug : bool
        if True then the cost of each round will be printed (default: True)

    Returns
    -------
    tuple : (list, list, np.ndarray, np.ndarray)
        list of cluster centers for each subspace
        list containing projections for each subspace
        orthogonal rotation matrix
        weights for softmax function to get beta values.
    """
    return nrkmeans_init(data=data, n_clusters=n_clusters, rounds=rounds, max_iter=5,
                         input_centers=input_centers, P=P, V=V, random_state=random_state, debug=debug)


def _determine_sgd_init_costs(enrc: _ENRC_Module, dataloader: torch.utils.data.DataLoader,
                              loss_fn: torch.nn.modules.loss._Loss, device: torch.device) -> float:
    """
    Determine the initial sgd costs.

    Parameters
    ----------
    enrc : _ENRC_Module
        The ENRC module
    dataloader : torch.utils.data.DataLoader
        dataloader to be used for the calculation of the costs
    loss_fn : torch.nn.modules.loss._Loss
        loss function for the reconstruction
    device : torch.device
        device to be trained on

    Returns
    -------
    cost : float
        the costs
    """
    cost = 0
    with torch.no_grad():
        for batch in dataloader:
            batch = batch[1].to(device)
            subspace_loss, _, batch_rot_back, _ = enrc(batch)
            rec_loss = loss_fn(batch_rot_back, batch)
            cost += (subspace_loss + rec_loss)
        cost /= len(dataloader)
    return cost.item()


def sgd_init(data: np.ndarray, n_clusters: list, learning_rate: float, batch_size: int = 128,
             optimizer_class: torch.optim.Optimizer = None, rounds: int = 2, epochs: int = 10,
             random_state: np.random.RandomState = None, input_centers: list = None, P: list = None,
             V: np.ndarray = None, device: torch.device = torch.device("cpu"), debug: bool = True) -> (
        list, list, np.ndarray, np.ndarray):
    """
    Initialization strategy based on optimizing ENRC's parameters V and beta in isolation from the autoencoder using a mini-batch gradient descent optimizer.
    This initialization strategy scales better to large data sets than the nrkmeans_init and only constraints V using the reconstruction error (torch.nn.MSELoss),
    which can be more flexible than the orthogonality constraint of NrKmeans. A problem of the sgd_init strategy is that it can be less stable for small data sets.

    Parameters
    ----------
    data : np.ndarray
        input data
    n_clusters : list
        list of ints, number of clusters for each clustering
    learning_rate : float
        learning rate for optimizer_class that is used to optimize V and beta
    batch_size : int
        size of the data batches (default: 128)
    optimizer_class : torch.optim.Optimizer
        optimizer for training. If None then torch.optim.Adam will be used (default: None)
    rounds : int
        number of repetitions of the initialization procedure (default: 2)
    epochs : int
        number of epochs for the actual clustering procedure (default: 10)
    random_state : np.random.RandomState
        random state for reproducible results (default: None)
    input_centers : list
        list of np.ndarray, default=None, optional parameter if initial cluster centers want to be set (optional)
    P : list
        list containing projections for each subspace (optional) (default: None)
    V : np.ndarray
        orthogonal rotation matrix (optional) (default: None)
    device : torch.device
        device on which should be trained on (default: torch.device('cpu'))
    debug : bool
        if True then the cost of each round will be printed (default: True)

    Returns
    -------
    tuple : (list, list, np.ndarray, np.ndarray)
        list of cluster centers for each subspace,
        list containing projections for each subspace,
        orthogonal rotation matrix,
        weights for softmax function to get beta values.
    """
    best = None
    lowest = np.inf
    dataloader = get_dataloader(data, batch_size=batch_size, shuffle=True, drop_last=True)

    for round_i in range(rounds):
        random_state = check_random_state(random_state)
        # start with random initialization
        init_centers, P_init, V_init, _ = random_nrkmeans_init(data=data, n_clusters=n_clusters, rounds=10,
                                                               input_centers=input_centers,
                                                               P=P, V=V, debug=False)

        # Initialize betas with uniform distribution
        enrc_module = _ENRC_Module(init_centers, P_init, V_init, beta_init_value=1.0 / len(P_init)).to_device(device)
        enrc_module.to_device(device)
        param_dict = [{'params': [enrc_module.V],
                       'lr': learning_rate},
                      {'params': [enrc_module.beta_weights],
                       'lr': learning_rate * 10},
                      ]
        if optimizer_class is None:
            optimizer_class = torch.optim.Adam
        optimizer = optimizer_class(param_dict)
        # Training loop
        # For the initialization we increase the weight for the rec error to enforce close to orthogonal V by setting fix_rec_error=True
        enrc_module.fit(data=data,
                        optimizer=optimizer,
                        max_epochs=epochs,
                        model=_IdentityAutoencoder(),
                        loss_fn=torch.nn.MSELoss(),
                        batch_size=batch_size,
                        device=device,
                        debug=False,
                        fix_rec_error=True)

        cost = _determine_sgd_init_costs(enrc=enrc_module, dataloader=dataloader, loss_fn=torch.nn.MSELoss(),
                                         device=device)
        if lowest > cost:
            best = [enrc_module.centers, enrc_module.P, enrc_module.V, enrc_module.beta_weights]
            lowest = cost
        if debug:
            print(f"Round {round_i}: Found solution with: {cost} (current best: {lowest})")

    centers, P, V, beta_weights = best
    beta_weights = calculate_beta_weight(data=torch.from_numpy(data).float(), centers=centers, V=V, P=P)
    centers = [centers_i.detach().cpu().numpy() for centers_i in centers]
    beta_weights = beta_weights.detach().cpu().numpy()
    V = V.detach().cpu().numpy()
    return centers, P, V, beta_weights


def enrc_init(data: np.ndarray, n_clusters: list, init: str = "auto", rounds: int = 10, input_centers: list = None,
              P: list = None, V: np.ndarray = None, random_state: np.random.RandomState = None, max_iter: int = 100,
              learning_rate: float = None, optimizer_class: torch.optim.Optimizer = None, batch_size: int = 128,
              epochs: int = 10, device: torch.device = torch.device("cpu"), debug: bool = True,
              init_kwargs: dict = None) -> (list, list, np.ndarray, np.ndarray):
    """
    Initialization strategy for the ENRC algorithm.

    Parameters
    ----------
    data : np.ndarray
        input data
    n_clusters : list
        list of ints, number of clusters for each clustering
    init : str
        {'nrkmeans', 'random', 'sgd', 'auto'} or callable. Initialization strategies for parameters cluster_centers, V and beta of ENRC. (default='auto')

        'nrkmeans' : Performs the NrKmeans algorithm to get initial parameters. This strategy is preferred for small data sets,
        but the orthogonality constraint on V and subsequently for the clustered subspaces can be sometimes to limiting in practice,
        e.g., if clusterings in the data are not perfectly non-redundant.

        'random' : Same as 'nrkmeans', but max_iter is set to 10, so the performance is faster, but also less optimized, thus more random.

        'sgd' : Initialization strategy based on optimizing ENRC's parameters V and beta in isolation from the autoencoder using a mini-batch gradient descent optimizer.
        This initialization strategy scales better to large data sets than the 'nrkmeans' option and only constraints V using the reconstruction error (torch.nn.MSELoss),
        which can be more flexible than the orthogonality constraint of NrKmeans. A problem of the 'sgd' strategy is that it can be less stable for small data sets.

        'auto' : Selects 'sgd' init if data.shape[0] > 100,000 or data.shape[1] > 1,000. For smaller data sets 'nrkmeans' init is used.

        If a callable is passed, it should take arguments data and n_clusters (additional parameters can be provided via the dictionary init_kwargs) and return an initialization (centers, P, V and beta_weights).
    
    rounds : int
        number of repetitions of the initialization procedure (default: 10)
    input_centers : list
        list of np.ndarray, optional parameter if initial cluster centers want to be set (optional) (default: None)
    P : list
        list containing projections for each subspace (optional) (default: None)
    V : np.ndarray
        orthogonal rotation matrix (optional) (default: None)
    random_state : np.random.RandomState
        random state for reproducible results (default: None)
    max_iter : int
        maximum number of iterations of NrKmeans.  Only used for init='nrkmeans' (default: 100)
    learning_rate : float
        learning rate for optimizer_class that is used to optimize V and beta. Only used for init='sgd'.
    optimizer_class : torch.optim.Optimizer
        optimizer for training. If None then torch.optim.Adam will be used. Only used for init='sgd' (default: None)
    batch_size : int
        size of the data batches. Only used for init='sgd' (default: 128)
    epochs : int
        number of epochs for the actual clustering procedure. Only used for init='sgd' (default: 10)
    device : torch.device
        device on which should be trained on. Only used for init='sgd' (default: torch.device('cpu'))
    debug : bool
        if True then the cost of each round will be printed (default: True)
    init_kwargs : dict
        additional parameters that are used if init is a callable (optional) (default: None)

    Returns
    -------
    tuple : (list, list, np.ndarray, np.ndarray)
        list of cluster centers for each subspace
        list containing projections for each subspace
        orthogonal rotation matrix
        weights for softmax function to get beta values.

    Raises
    ----------
    ValueError : if init variable is passed that is not implemented.
    """
    if init == "nrkmeans":
        centers, P, V, beta_weights = nrkmeans_init(data=data, n_clusters=n_clusters, rounds=rounds,
                                                    input_centers=input_centers, P=P, V=V, random_state=random_state,
                                                    debug=debug)
    elif init == "random":
        centers, P, V, beta_weights = random_nrkmeans_init(data=data, n_clusters=n_clusters, rounds=rounds,
                                                           input_centers=input_centers, P=P, V=V,
                                                           random_state=random_state, debug=debug)
    elif init == "sgd":
        centers, P, V, beta_weights = sgd_init(data=data, n_clusters=n_clusters, learning_rate=learning_rate,
                                               rounds=rounds, epochs=epochs, input_centers=input_centers, P=P, V=V,
                                               optimizer_class=optimizer_class, batch_size=batch_size,
                                               random_state=random_state, device=device, debug=debug)
    elif init == "auto":
        if data.shape[0] > 100000 or data.shape[1] > 1000:
            init = "sgd"
        else:
            init = "nrkmeans"
        centers, P, V, beta_weights = enrc_init(data=data, n_clusters=n_clusters, device=device, init=init,
                                                rounds=rounds, input_centers=input_centers,
                                                P=P, V=V, random_state=random_state, max_iter=max_iter,
                                                learning_rate=learning_rate, optimizer_class=optimizer_class,
                                                epochs=epochs, debug=debug)
    elif callable(init):
        if init_kwargs is not None:
            centers, P, V, beta_weights = init(data, n_clusters, **init_kwargs)
        else:
            centers, P, V, beta_weights = init(data, n_clusters)
    else:
        raise ValueError(f"init={init} is not implemented.")
    return centers, P, V, beta_weights


"""
===================== Cluster Reinitialization Strategy =====================
"""


def _calculate_rotated_embeddings_and_distances_for_n_samples(enrc: _ENRC_Module, model: torch.nn.Module,
                                                              dataloader: torch.utils.data.DataLoader, n_samples: int,
                                                              center_id: int, subspace_id: int, device: torch.device,
                                                              calc_distances: bool = True) -> (
        torch.Tensor, torch.Tensor):
    """
    Helper function for calculating the distances and embeddings for n_samples in a mini-batch fashion.

    Parameters
    ----------
    enrc : _ENRC_Module
        The ENRC Module
    model : torch.nn.Module
        The autoencoder
    dataloader : torch.utils.data.DataLoader
        dataloader from which data is randomly sampled
    n_samples : int
        the number of samples
    center_id : int
        the id of the center
    subspace_id : int
        the id of the subspace
    device : torch.device
        device to be trained on
    calc_distances : bool
        specifies if the distances between all not lonely centers to embedded data points should be calculated

    Returns
    -------
    tuple : (torch.Tensor, torch.Tensor)
        the rotated embedded data points
        the distances (if calc_distancesis True)
    """
    changed = True
    sample_count = 0
    subspace_betas = enrc.subspace_betas()[subspace_id, :]
    subspace_centers = enrc.centers[subspace_id]
    embedding_rot = []
    dists = []
    for batch in dataloader:
        batch = batch[1].to(device)
        if (batch.shape[0] + sample_count) > n_samples:
            # Remove samples from the batch that are too many.
            # Assumes that dataloader randomly samples minibatches, 
            # so removing the last objects does not matter
            diff = (batch.shape[0] + sample_count) - n_samples
            batch = batch[:-diff]
        z_rot = enrc.rotate(model.encode(batch))
        embedding_rot.append(z_rot.detach().cpu())

        if calc_distances:
            # Calculate distance from all not lonely centers to embedded data points
            idx_other_centers = [i for i in range(subspace_centers.shape[0]) if i != center_id]
            weighted_squared_diff = squared_euclidean_distance(z_rot, subspace_centers[idx_other_centers],
                                                               weights=subspace_betas)
            dists.append(weighted_squared_diff.detach().cpu())

        # Increase sample_count by batch size. 
        sample_count += batch.shape[0]
        if sample_count >= n_samples:
            break
    embedding_rot = torch.cat(embedding_rot, 0)
    if calc_distances:
        dists = torch.cat(dists, 0)
    else:
        dists = None
    return embedding_rot, dists


def _split_most_expensive_cluster(distances: torch.Tensor, z: torch.Tensor) -> torch.Tensor:
    """
    Splits most expensive cluster calculated based on the k-means loss and returns a new centroid.
    The new centroid is the one which is worst represented (largest distance) by the most expensive cluster centroid.

    Parameters
    ----------
    distances : torch.Tensor
        n x n distance matrix, where n is the size of the mini-batch.
    z : torch.Tensor
        n x d embedded data point, where n is the size of the mini-batch and d is the dimensionality of the embedded space.

    Returns
    -------
    center : torch.Tensor
        new center
    """
    kmeans_loss = distances.sum(0)
    costly_centroid_idx = kmeans_loss.argmax()
    max_idx = distances[costly_centroid_idx, :].argmax()
    return z[max_idx]


def _random_reinit_cluster(embedded: torch.Tensor) -> torch.Tensor:
    """
    Reinitialize random cluster centers.

    Parameters
    ----------
    embedded : torch.Tensor
        The embedded data points

    Returns
    -------
    center : torch.Tensor
        The random center
    """
    rand_indices = np.random.randint(low=0, high=embedded.shape[0], size=1)
    random_perturbation = torch.empty_like(embedded[rand_indices]).normal_(mean=embedded.mean().item(),
                                                                           std=embedded.std().item())
    center = embedded[rand_indices] + 0.0001 * random_perturbation
    return center


def reinit_centers(enrc: _ENRC_Module, subspace_id: int, dataloader: torch.utils.data.DataLoader,
                   model: torch.nn.Module,
                   n_samples: int = 512, kmeans_steps: int = 10, split: str = "random") -> None:
    """
    Reinitializes centers that have been lost, i.e. if they did not get any data point assigned. Before a center is reinitialized,
    this method checks whether a center has not get any points assigned over several mini-batch iterations and if this count is higher than
    enrc.reinit_threshold the center will be reinitialized.
    
    Parameters
    ----------
    enrc : _ENRC_Module
        torch.nn.Module instance for the ENRC algorithm
    subspace_id : int
        integer which indicates which subspace the cluster to be checked are in.
    dataloader : torch.utils.data.DataLoader
        dataloader from which data is randomly sampled. Important shuffle=True needs to be set, because n_samples random samples are drawn.
    model : torch.nn.Module
        autoencoder model used for the embedding
    n_samples : int
        number of samples that should be used for the reclustering (default: 512)
    kmeans_steps : int
        number of mini-batch kmeans steps that should be conducted with the new centroid (default: 10)
    split : str
        {'random', 'cost'}, default='random', select how clusters should be split for renitialization.
        'random' : split a random point from the random sample of size=n_samples.
        'cost' : split the cluster with max kmeans cost.
    """
    N = len(dataloader.dataset)
    if n_samples > N:
        print(f"WARNING: n_samples={n_samples} > number of data points={N}. Set n_samples=number of data points")
        n_samples = N
    # Assumes that enrc and model are on the same device
    device = enrc.V.device
    with torch.no_grad():
        k = enrc.centers[subspace_id].shape[0]
        subspace_betas = enrc.subspace_betas()
        for center_id, count_i in enumerate(enrc.lonely_centers_count[subspace_id].flatten()):
            if count_i > enrc.reinit_threshold:
                print(f"Reinitialize cluster {center_id} in subspace {subspace_id}")
                if split == "cost":
                    embedding_rot, dists = _calculate_rotated_embeddings_and_distances_for_n_samples(enrc, model,
                                                                                                     dataloader,
                                                                                                     n_samples,
                                                                                                     center_id,
                                                                                                     subspace_id,
                                                                                                     device)
                    new_center = _split_most_expensive_cluster(distances=dists, z=embedding_rot)
                elif split == "random":
                    embedding_rot, _ = _calculate_rotated_embeddings_and_distances_for_n_samples(enrc, model,
                                                                                                 dataloader, n_samples,
                                                                                                 center_id, subspace_id,
                                                                                                 device,
                                                                                                 calc_distances=False)
                    new_center = _random_reinit_cluster(embedding_rot)
                else:
                    raise NotImplementedError(f"split={split} is not implemented. Has to be 'cost' or 'random'.")
                enrc.centers[subspace_id][center_id, :] = new_center.to(device)

                embeddingloader = torch.utils.data.DataLoader(embedding_rot, batch_size=dataloader.batch_size,
                                                              shuffle=False, drop_last=False)
                # perform mini-batch kmeans steps
                batch_cluster_sums = 0
                mask_sum = 0
                for step_i in range(kmeans_steps):
                    for z_rot in embeddingloader:
                        z_rot = z_rot.to(device)
                        weighted_squared_diff = squared_euclidean_distance(z_rot, enrc.centers[subspace_id],
                                                                           weights=subspace_betas[subspace_id, :])
                        assignments = weighted_squared_diff.detach().argmin(1)
                        one_hot_mask = int_to_one_hot(assignments, k)
                        batch_cluster_sums += (z_rot.unsqueeze(1) * one_hot_mask.unsqueeze(2)).sum(0)
                        mask_sum += one_hot_mask.sum(0)
                    nonzero_mask = (mask_sum != 0)
                    enrc.centers[subspace_id][nonzero_mask] = batch_cluster_sums[nonzero_mask] / mask_sum[
                        nonzero_mask].unsqueeze(1)
                    # Reset mask_sum
                    enrc.mask_sum[subspace_id] = mask_sum.unsqueeze(1)
                # lonely_centers_count is reset
                enrc.lonely_centers_count[subspace_id][center_id] = 0


"""
===================== ENRC  =====================
"""


def _are_labels_equal(labels_new: np.ndarray, labels_old: np.ndarray, threshold: float = None) -> bool:
    """
    Check if the old labels and new labels are equal. Therefore check the nmi for each subspace_nr. If all are 1, labels
    have not changed.
    
    Parameters
    ----------
    labels_new: np.ndarray
        new labels list
    labels_old: np.ndarray
        old labels list
    threshold: float
        specifies how close the two labelings should match (default: None)

    Returns
    ----------
    changed : bool
        True if labels for all subspaces are the same
    """
    if labels_new is None or labels_old is None or labels_new.shape[1] != labels_old.shape[1]:
        return False

    if threshold is None:
        v = 1
    else:
        v = 1 - threshold
    return all(
        [normalized_mutual_info_score(labels_new[:, i], labels_old[:, i], average_method="arithmetic") >= v for i in
         range(labels_new.shape[1])])


def _enrc(X: np.ndarray, n_clusters: list, V: np.ndarray, P: list, input_centers: list, batch_size: int,
          pretrain_learning_rate: float, clustering_learning_rate: float, pretrain_epochs: int, clustering_epochs: int,
          optimizer_class: torch.optim.Optimizer, loss_fn: torch.nn.modules.loss._Loss,
          degree_of_space_distortion: float, degree_of_space_preservation: float, autoencoder: torch.nn.Module,
          embedding_size: int, init: str, random_state: np.random.RandomState, device: torch.device,
          scheduler: torch.optim.lr_scheduler, scheduler_params: dict, tolerance_threshold: float, init_kwargs: dict,
          init_subsample_size: int, debug: bool) -> (
        np.ndarray, list, np.ndarray, list, np.ndarray, list, list, torch.nn.Module):
    """
    Start the actual ENRC clustering procedure on the input data set.

    Parameters
    ----------
    X : np.ndarray
        input data
    n_clusters : list
        list containing number of clusters for each clustering
    V : np.ndarray
        orthogonal rotation matrix
    P : list
        list containing projections for each clustering
    input_centers : list
        list containing the cluster centers for each clustering
    batch_size : int
        size of the data batches
    pretrain_learning_rate : float
        learning rate for the pretraining of the autoencoder
    clustering_learning_rate: float
        learning rate of the actual clustering procedure
    pretrain_epochs : int
        number of epochs for the pretraining of the autoencoder
    clustering_epochs : int
        maximum number of epochs for the actual clustering procedure
    optimizer_class : torch.optim.Optimizer
        optimizer for pretraining and training
    loss_fn : torch.nn.modules.loss._Loss
        loss function for the reconstruction
    degree_of_space_distortion : float
        weight of the cluster loss term. The higher it is set the more the embedded space will be shaped to the assumed cluster structure
    degree_of_space_preservation : float
        weight of regularization loss term, e.g., reconstruction loss
    autoencoder : torch.nn.Module
         the input autoencoder. If None a new autoencoder will be created and trained
    embedding_size : int
        size of the embedding within the autoencoder. Only used if autoencoder is None
    init : str
        strchoose which initialization strategy should be used. Has to be one of 'nrkmeans', 'random' or 'sgd'.
    random_state : np.random.RandomState
        use a fixed random state to get a repeatable solution
    device : torch.device
        if device is None then it will be checked whether a gpu is available or not
    scheduler : torch.optim.lr_scheduler
        learning rate scheduler that should be used
    scheduler_params : dict
        dictionary of the parameters of the scheduler object
    tolerance_threshold : float
        tolerance threshold to determine when the training should stop. If the NMI(old_labels, new_labels) >= (1-tolerance_threshold)
        for all clusterings then the training will stop before max_epochs is reached. If set high than training will stop earlier then max_epochs, and if set to 0 or None the training
        will train as long as the labels are not changing anymore.
    init_kwargs : dict
        additional parameters that are used if init is a callable
    init_subsample_size : int
        specify if only a subsample of size 'init_subsample_size' of the data should be used for the initialization
    debug : bool
        if True additional information during the training will be printed

    Returns
    -------
    tuple : (np.ndarray, list, np.ndarray, list, np.ndarray, list, list, torch.nn.Module)
        the cluster labels,
        the cluster centers,
        the orthogonal rotation matrix,
        the dimensionalities of the subspaces,
        the betas,
        the projections of the subspaces,
        the final n_clusters,
        the final autoencoder
    """
    # Set device to train on
    if device is None:
        device = detect_device()

    # Setup dataloaders
    trainloader = get_dataloader(X, batch_size=batch_size, shuffle=True, drop_last=True)
    testloader = get_dataloader(X, batch_size=batch_size, shuffle=False, drop_last=False)

    # Use subsample of the data if specified
    if init_subsample_size is not None and init_subsample_size > 0:
        rng = np.random.default_rng(random_state)
        rand_idx = rng.choice(X.shape[0], init_subsample_size, replace=False)
        subsampleloader = get_dataloader(X[rand_idx], batch_size=batch_size, shuffle=False, drop_last=False)
    else:
        subsampleloader = testloader

    # Setup autoencoder
    autoencoder = get_trained_autoencoder(trainloader, pretrain_learning_rate, pretrain_epochs, device,
                                          optimizer_class, loss_fn, X.shape[1], embedding_size, autoencoder)

    embedded_data = encode_batchwise(subsampleloader, autoencoder, device)

    # Run ENRC init
    print("Run ENRC init: ", init)
    input_centers, P, V, beta_weights = enrc_init(data=embedded_data, n_clusters=n_clusters, device=device, init=init,
                                                  rounds=10, epochs=10, batch_size=batch_size, debug=debug,
                                                  input_centers=input_centers, P=P, V=V, random_state=random_state,
                                                  max_iter=100, learning_rate=clustering_learning_rate,
                                                  optimizer_class=optimizer_class, init_kwargs=init_kwargs)
    # Setup ENRC Module
    enrc_module = _ENRC_Module(input_centers, P, V, degree_of_space_distortion=degree_of_space_distortion,
                               degree_of_space_preservation=degree_of_space_preservation,
                               beta_weights=beta_weights).to_device(device)

    param_dict = [{'params': autoencoder.parameters(),
                   'lr': clustering_learning_rate},
                  {'params': [enrc_module.V],
                   'lr': clustering_learning_rate},
                  # In accordance to the original paper we update the betas 10 times faster
                  {'params': [enrc_module.beta_weights],
                   'lr': clustering_learning_rate * 10},
                  ]
    optimizer = optimizer_class(param_dict)

    if scheduler is not None:
        scheduler = scheduler(optimizer, **scheduler_params)

    # Training loop
    print("Start ENRC training")
    enrc_module.fit(data=X,
                    max_epochs=clustering_epochs,
                    optimizer=optimizer,
                    loss_fn=loss_fn,
                    batch_size=batch_size,
                    model=autoencoder,
                    device=device,
                    scheduler=scheduler,
                    tolerance_threshold=tolerance_threshold,
                    debug=debug)

    # Recluster
    print("Recluster")
    enrc_module.recluster(dataloader=subsampleloader, model=autoencoder, device=device)
    # Predict labels and transfer other parameters to numpy
    cluster_labels = enrc_module.predict_batchwise(model=autoencoder, dataloader=testloader, device=device, use_P=True)
    cluster_centers = [centers_i.detach().cpu().numpy() for centers_i in enrc_module.centers]
    V = enrc_module.V.detach().cpu().numpy()
    betas = enrc_module.subspace_betas().detach().cpu().numpy()
    P = enrc_module.P
    m = enrc_module.m
    return cluster_labels, cluster_centers, V, m, betas, P, n_clusters, autoencoder


class ENRC(BaseEstimator, ClusterMixin):
    """
    The Embeddedn Non-Redundant Clustering (ENRC) algorithm.
        
    Parameters
    ----------
    n_clusters : list
        list containing number of clusters for each clustering
    V : np.ndarray
        orthogonal rotation matrix (optional) (default: None)
    P : list
        list containing projections for each clustering (optional) (default: None)
    input_centers : list
        list containing the cluster centers for each clustering (optional) (default: None)
    batch_size : int
        size of the data batches (default: 128)
    pretrain_learning_rate : float
        learning rate for the pretraining of the autoencoder (default: 1e-3)
    clustering_learning_rate : float
        learning rate of the actual clustering procedure (default: 1e-4)
    pretrain_epochs : int
        number of epochs for the pretraining of the autoencoder (default: 100)
    clustering_epochs : int
        maximum number of epochs for the actual clustering procedure (default: 150)
    tolerance_threshold : float
        tolerance threshold to determine when the training should stop. If the NMI(old_labels, new_labels) >= (1-tolerance_threshold)
        for all clusterings then the training will stop before max_epochs is reached. If set high than training will stop earlier then max_epochs, and if set to 0 or None the training
        will train as long as the labels are not changing anymore (default: None)
    optimizer_class : torch.optim.Optimizer
        optimizer for pretraining and training (default: torch.optim.Adam)
    loss_fn : torch.nn.modules.loss._Loss
        loss function for the reconstruction (default: torch.nn.MSELoss())
    degree_of_space_distortion : float
        weight of the cluster loss term. The higher it is set the more the embedded space will be shaped to the assumed cluster structure (default: 1.0)
    degree_of_space_preservation : float
        weight of regularization loss term, e.g., reconstruction loss (default: 1.0)
    autoencoder : torch.nn.Module
        the input autoencoder. If None a new autoencoder will be created and trained (default: None)
    embedding_size : int
        size of the embedding within the autoencoder. Only used if autoencoder is None (default: 20)
    init : str
        choose which initialization strategy should be used. Has to be one of 'nrkmeans', 'random' or 'sgd' (default: 'nrkmeans')
    random_state : np.random.RandomState
        use a fixed random state to get a repeatable solution. Can also be of type int (default: None)
    device : torch.device
        if device is None then it will be checked whether a gpu is available or not (default: None)
    scheduler : torch.optim.lr_scheduler
        learning rate scheduler that should be used (default: None)
    scheduler_params : dict
        dictionary of the parameters of the scheduler object (default: None)
    init_kwargs : dict
        additional parameters that are used if init is a callable (optional) (default: None)
    init_subsample_size: int
        specify if only a subsample of size 'init_subsample_size' of the data should be used for the initialization (optional) (default: None)
    debug: bool
        if True additional information during the training will be printed (default: False)

    Attributes
    ----------
    labels_ : np.ndarray
        The final labels
    cluster_centers_ : np.ndarray
        The final cluster centers
    autoencoder : torch.nn.Module
        The final autoencoder

    Raises
    ----------
    ValueError : if init is not one of 'nrkmeans', 'random', 'auto' or 'sgd'.

    References
    ----------
    Miklautz, Lukas & Dominik Mautz et al. "Deep embedded non-redundant clustering."
    Proceedings of the AAAI Conference on Artificial Intelligence. Vol. 34. No. 04. 2020.
    """

    def __init__(self, n_clusters: list, V: np.ndarray = None, P: list = None, input_centers: list = None,
                 batch_size: int = 128, pretrain_learning_rate: float = 1e-3,
                 clustering_learning_rate: float = 1e-4, pretrain_epochs: int = 100, clustering_epochs: int = 150,
                 tolerance_threshold: float = None, optimizer_class: torch.optim.Optimizer = torch.optim.Adam,
                 loss_fn: torch.nn.modules.loss._Loss = torch.nn.MSELoss(),
                 degree_of_space_distortion: float = 1.0, degree_of_space_preservation: float = 1.0,
                 autoencoder: torch.nn.Module = None, embedding_size: int = 20, init: str = "nrkmeans",
                 device: torch.device = None, scheduler: torch.optim.lr_scheduler = None,
                 scheduler_params: dict = None, init_kwargs: dict = None, init_subsample_size: int = None,
                 random_state: np.random.RandomState = None, debug: bool = False):
        self.n_clusters = n_clusters.copy()
        self.device = device
        self.batch_size = batch_size
        self.pretrain_learning_rate = pretrain_learning_rate
        self.clustering_learning_rate = clustering_learning_rate
        self.pretrain_epochs = pretrain_epochs
        self.clustering_epochs = clustering_epochs
        self.tolerance_threshold = tolerance_threshold
        self.optimizer_class = optimizer_class
        self.loss_fn = loss_fn
        self.degree_of_space_distortion = degree_of_space_distortion
        self.degree_of_space_preservation = degree_of_space_preservation
        self.autoencoder = autoencoder
        self.embedding_size = embedding_size
        self.scheduler = scheduler
        self.scheduler_params = scheduler_params
        self.init_kwargs = init_kwargs
        self.init_subsample_size = init_subsample_size
        self.random_state = check_random_state(random_state)
        set_torch_seed(self.random_state)
        self.debug = debug

        if len(self.n_clusters) < 2:
            raise ValueError(f"n_clusters={n_clusters}, but should be <= 2.")

        if init in available_init_strategies():
            self.init = init
        else:
            raise ValueError(f"init={init} does not exist, has to be one of {available_init_strategies()}.")
        self.input_centers = input_centers
        self.V = V
        self.m = None
        self.P = P

    def fit(self, X: np.ndarray, y: np.ndarray = None) -> 'ENRC':
        """
        Cluster the input dataset with the ENRC algorithm. Saves the labels, centers, V, m, Betas, and P
        in the ENRC object.
        The resulting cluster labels will be stored in the labels_ attribute.

        Parameters
        ----------
        X : np.ndarray
            input data
        y : np.ndarray
            the labels (can be ignored)
            
        Returns
        ----------
        self : ENRC
            returns the ENRC object
        """
        cluster_labels, cluster_centers, V, m, betas, P, n_clusters, autoencoder = _enrc(X=X,
                                                                                         n_clusters=self.n_clusters,
                                                                                         V=self.V,
                                                                                         P=self.P,
                                                                                         input_centers=self.input_centers,
                                                                                         batch_size=self.batch_size,
                                                                                         pretrain_learning_rate=self.pretrain_learning_rate,
                                                                                         clustering_learning_rate=self.clustering_learning_rate,
                                                                                         pretrain_epochs=self.pretrain_epochs,
                                                                                         clustering_epochs=self.clustering_epochs,
                                                                                         tolerance_threshold=self.tolerance_threshold,
                                                                                         optimizer_class=self.optimizer_class,
                                                                                         loss_fn=self.loss_fn,
                                                                                         degree_of_space_distortion=self.degree_of_space_distortion,
                                                                                         degree_of_space_preservation=self.degree_of_space_preservation,
                                                                                         autoencoder=self.autoencoder,
                                                                                         embedding_size=self.embedding_size,
                                                                                         init=self.init,
                                                                                         random_state=self.random_state,
                                                                                         device=self.device,
                                                                                         scheduler=self.scheduler,
                                                                                         scheduler_params=self.scheduler_params,
                                                                                         init_kwargs=self.init_kwargs,
                                                                                         init_subsample_size=self.init_subsample_size,
                                                                                         debug=self.debug)
        # Update class variables
        self.labels_ = cluster_labels
        self.cluster_centers_ = cluster_centers
        self.V = V
        self.m = m
        self.P = P
        self.betas = betas
        self.n_clusters = n_clusters
        self.autoencoder = autoencoder
        return self

    def predict(self, X: np.ndarray, y: np.ndarray = None, use_P: bool = True) -> np.ndarray:
        """
        Predicts the labels for each clustering of X in a mini-batch manner.
        
        Parameters
        ----------
        X : np.ndarray
            input data
        y : np.ndarray
            the labels (can be ignored)
        use_P: bool
            if True then P will be used to hard select the dimensions for each clustering, else the soft beta weights are used (default: True)
        
        Returns
        -------
        predicted_labels : np.ndarray
            n x c matrix, where n is the number of data points in X and c is the number of clusterings.
        """
        dataloader = get_dataloader(X, batch_size=self.batch_size, shuffle=False, drop_last=False)

        self.autoencoder.to(self.device)
        predicted_labels = enrc_predict_batchwise(V=torch.from_numpy(self.V).float().to(self.device),
                                                  centers=[torch.from_numpy(c).float().to(self.device) for c in
                                                           self.cluster_centers_],
                                                  subspace_betas=torch.from_numpy(self.betas).float().to(self.device),
                                                  model=self.autoencoder,
                                                  dataloader=dataloader,
                                                  device=self.device,
                                                  use_P=use_P)
        return predicted_labels

    def transform_full_space(self, X: np.ndarray, embedded=False) -> np.ndarray:
        """
        Embedds the input dataset with the autoencoder and the matrix V from the ENRC object.
        Parameters
        ----------
        X : np.ndarray
            input data
        embedded : bool
            if True, then X is assumed to be already embedded (default: False)
        
        Returns
        -------
        rotated : np.ndarray
            The transformed data
        """
        if not embedded:
            dataloader = get_dataloader(X, batch_size=self.batch_size, shuffle=False, drop_last=False)
            emb = encode_batchwise(dataloader=dataloader, module=self.autoencoder, device=self.device)
        else:
            emb = X
        rotated = np.matmul(emb, self.V)
        return rotated

    def transform_subspace(self, X: np.ndarray, subspace_index: int, embedded: bool = False) -> np.ndarray:
        """
        Embedds the input dataset with the autoencoder and with the matrix V projected onto a special clusterspace_nr.
        
        Parameters
        ----------
        X : np.ndarray
            input data
        subspace_index: int
            index of the subspace_nr
        embedded: bool
            if True, then X is assumed to be already embedded (default: False)
        
        Returns
        -------
        subspace : np.ndarray
            The transformed subspace
        """
        if not embedded:
            dataloader = get_dataloader(X, batch_size=self.batch_size, shuffle=False, drop_last=False)
            emb = encode_batchwise(dataloader=dataloader, module=self.autoencoder, device=self.device)
        else:
            emb = X
        cluster_space_V = self.V[:, self.P[subspace_index]]
        subspace = np.matmul(emb, cluster_space_V)
        return subspace

    def plot_subspace(self, X: np.ndarray, subspace_index: int, labels: np.ndarray = None, plot_centers: bool = False,
                      gt: np.ndarray = None, equal_axis: bool = False) -> None:
        """
        Plot the specified subspace_nr as scatter matrix plot.
       
        Parameters
        ----------
        X : np.ndarray
            input data
        subspace_index: int, index of the subspace_nr
        labels: np.ndarray
            the labels to use for the plot (default: labels found by Nr-Kmeans) (default: None)
        plot_centers: bool
            plot centers if True (default: False)
        gt: np.ndarray
            of ground truth labels (default=None)
        equal_axis: bool
            equalize axis if True (default: False)
        Returns
        -------
        scatter matrix plot of the input data
        """
        if self.labels_ is None:
            raise Exception("The ENRC algorithm has not run yet. Use the fit() function first.")
        if labels is None:
            labels = self.labels_[:, subspace_index]
        if X.shape[0] != labels.shape[0]:
            raise Exception("Number of data objects must match the number of labels.")
        plot_scatter_matrix(self.transform_subspace(X, subspace_index), labels,
                            self.cluster_centers_[subspace_index] if plot_centers else None,
                            true_labels=gt, equal_axis=equal_axis)

    def reconstruct_subspace_centroids(self, subspace_index: int) -> np.ndarray:
        """
        Reconstructs the centroids in the specified subspace_nr.

        Parameters
        ----------
        subspace_index: int
            index of the subspace_nr

        Returns
        -------
        centers_rec : centers_rec
            reconstructed centers as np.ndarray
        """
        cluster_space_centers = self.cluster_centers_[subspace_index]
        # rotate back as centers are in the V-rotated space
        centers_rot_back = np.matmul(cluster_space_centers, self.V.transpose())
        centers_rec = self.autoencoder.decode(torch.from_numpy(centers_rot_back).float().to(self.device))
        return centers_rec.detach().cpu().numpy()
