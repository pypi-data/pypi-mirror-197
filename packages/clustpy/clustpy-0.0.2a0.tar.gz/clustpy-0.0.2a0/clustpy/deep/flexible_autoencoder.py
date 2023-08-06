"""
@authors:
Lukas Miklautz
"""

import torch
import numpy as np
from ._early_stopping import EarlyStopping
from ._data_utils import get_dataloader


class FullyConnectedBlock(torch.nn.Module):
    """
    Feed Forward Neural Network Block

    Parameters
    ----------
    layers : list
        list of the different layer sizes
    batch_norm : bool
        set True if you want to use torch.nn.BatchNorm1d (default: False)
    dropout : float
        set the amount of dropout you want to use (default: None)
    activation_fn : torch.nn.Module
        activation function from torch.nn, set the activation function for the hidden layers, if None then it will be linear (default: None)
    bias : bool
        set False if you do not want to use a bias term in the linear layers (default: None)
    output_fn : torch.nn.Module
        activation function from torch.nn, set the activation function for the last layer, if None then it will be linear (default: None)

    Attributes
    ----------
    block: torch.nn.Sequential
        feed forward neural network
    """

    def __init__(self, layers: list, batch_norm: bool = False, dropout: float = None,
                 activation_fn: torch.nn.Module = None, bias: bool = True, output_fn: torch.nn.Module = None):
        super(FullyConnectedBlock, self).__init__()
        self.layers = layers
        self.batch_norm = batch_norm
        self.dropout = dropout
        self.bias = bias
        self.activation_fn = activation_fn
        self.output_fn = output_fn

        fc_block_list = []
        for i in range(len(layers) - 1):
            fc_block_list.append(torch.nn.Linear(layers[i], layers[i + 1], bias=self.bias))
            if self.batch_norm:
                fc_block_list.append(torch.nn.BatchNorm1d(layers[i + 1]))
            if self.dropout is not None:
                fc_block_list.append(torch.nn.Dropout(self.dropout))
            if self.activation_fn is not None:
                # last layer is handled differently
                if (i != len(layers) - 2):
                    fc_block_list.append(activation_fn())
                else:
                    if self.output_fn is not None:
                        fc_block_list.append(self.output_fn())

        self.block = torch.nn.Sequential(*fc_block_list)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Pass a sample through the FullyConnectedBlock.

        Parameters
        ----------
        x : torch.Tensor
            the sample

        Returns
        -------
        forwarded : torch.Tensor
            The passed sample.
        """
        forwarded = self.block(x)
        return forwarded


class FlexibleAutoencoder(torch.nn.Module):
    """
    A flexible feedforward autoencoder.

    Parameters
    ----------
    layers : list
        list of the different layer sizes from input to embedding, e.g. an example architecture for MNIST [784, 512, 256, 10], where 784 is the input dimension and 10 the embedding dimension.
        If decoder_layers are not specified then the decoder is symmetric and goes in the same order from embedding to input.
    batch_norm : bool
        Set True if you want to use torch.nn.BatchNorm1d (default: False)
    dropout : float
        Set the amount of dropout you want to use (default: None)
    activation_fn : torch.nn.Module
        activation function from torch.nn, set the activation function for the hidden layers, if None then it will be linear (default: torch.nn.LeakyReLU)
    bias : bool
        set False if you do not want to use a bias term in the linear layers (default: True)
    decoder_layers : list
        list of different layer sizes from embedding to output of the decoder. If set to None, will be symmetric to layers (default: None)
    decoder_output_fn : torch.nn.Module
        activation function from torch.nn, set the activation function for the decoder output layer, if None then it will be linear.
        e.g. set to torch.nn.Sigmoid if you want to scale the decoder output between 0 and 1 (default: None)

    Attributes
    ----------
    encoder : FullyConnectedBlock
        encoder part of the autoencoder, responsible for embedding data points (class is FullyConnectedBlock)
    decoder : FullyConnectedBlock
        decoder part of the autoencoder, responsible for reconstructing data points from the embedding (class is FullyConnectedBlock)
    fitted  : bool
        boolean value indicating whether the autoencoder is already fitted.

    References
    ----------
    E.g. Ballard, Dana H. "Modular learning in neural networks." Aaai. Vol. 647. 1987.
    """

    def __init__(self, layers: list, batch_norm: bool = False, dropout: float = None,
                 activation_fn: torch.nn.Module = torch.nn.LeakyReLU, bias: bool = True, decoder_layers: list = None,
                 decoder_output_fn: torch.nn.Module = None):
        super(FlexibleAutoencoder, self).__init__()
        self.fitted = False
        if decoder_layers is None:
            decoder_layers = layers[::-1]
        if (layers[-1] != decoder_layers[0]):
            raise ValueError(
                f"Innermost hidden layer and first decoder layer do not match, they are {layers[-1]} and {decoder_layers[0]} respectively.")
        if (layers[0] != decoder_layers[-1]):
            raise ValueError(
                f"Output and input dimension do not match, they are {layers[0]} and {decoder_layers[-1]} respectively.")
        # Initialize encoder
        self.encoder = FullyConnectedBlock(layers=layers, batch_norm=batch_norm, dropout=dropout,
                                           activation_fn=activation_fn, bias=bias, output_fn=None)

        # Inverts the list of layers to make symmetric version of the encoder
        self.decoder = FullyConnectedBlock(layers=decoder_layers, batch_norm=batch_norm, dropout=dropout,
                                           activation_fn=activation_fn, bias=bias,
                                           output_fn=decoder_output_fn)

    def encode(self, x: torch.Tensor) -> torch.Tensor:
        """
        Apply the encoder function to x.

        Parameters
        ----------
        x : torch.Tensor
            input data point, can also be a mini-batch of points
        
        Returns
        -------
        embedded : torch.Tensor
            the embedded data point with dimensionality embedding_size
        """
        assert x.shape[1] == self.encoder.layers[0], "Input layer of the encoder does not match input sample"
        embedded = self.encoder(x)
        return embedded

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
        assert embedded.shape[1] == self.decoder.layers[0], "Input layer of the decoder does not match input sample"
        decoded = self.decoder(embedded)
        return decoded

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

    def loss(self, batch: list, loss_fn: torch.nn.modules.loss._Loss, device: torch.device) -> torch.Tensor:
        """
        Calculate the loss of a single batch of data.

        Parameters
        ----------
        batch: list
            the different parts of a dataloader (id, samples, ...)
        loss_fn : torch.nn.modules.loss._Loss
            loss function to be used for reconstruction
        device : torch.device
            device to be trained on

        Returns
        -------
        loss : torch.Tensor
            returns the reconstruction loss of the input sample
        """
        assert type(batch) is list, "batch must come from a dataloader and therefore be of type list"
        batch_data = batch[1].to(device)
        reconstruction = self.forward(batch_data)
        loss = loss_fn(reconstruction, batch_data)
        return loss

    def evaluate(self, dataloader: torch.utils.data.DataLoader, loss_fn: torch.nn.modules.loss._Loss,
                 device: torch.device = torch.device("cpu")) -> torch.Tensor:
        """
        Evaluates the autoencoder.
        
        Parameters
        ----------
        dataloader : torch.utils.data.DataLoader
            dataloader to be used for training
        loss_fn : torch.nn.modules.loss._Loss
            loss function to be used for reconstruction
        device : torch.device
            device to be trained on (default: torch.device('cpu'))
        
        Returns
        -------
        loss: torch.Tensor
            returns the reconstruction loss of all samples in dataloader
        """
        with torch.no_grad():
            self.eval()
            loss = 0
            for batch in dataloader:
                loss += self.loss(batch, loss_fn, device)
            loss /= len(dataloader)
        return loss

    def fit(self, n_epochs: int, lr: float, batch_size: int = 128, data: np.ndarray = None,
            data_eval: np.ndarray = None,
            dataloader: torch.utils.data.DataLoader = None, evalloader: torch.utils.data.DataLoader = None,
            optimizer_class: torch.optim.Optimizer = torch.optim.Adam,
            loss_fn: torch.nn.modules.loss._Loss = torch.nn.MSELoss(), patience: int = 5,
            scheduler: torch.optim.lr_scheduler = None, scheduler_params: dict = None,
            device: torch.device = torch.device("cpu"), model_path: str = None,
            print_step: int = 0) -> 'FlexibleAutoencoder':
        """
        Trains the autoencoder in place.
        
        Parameters
        ----------
        n_epochs : int
            number of epochs for training
        lr : float
            learning rate to be used for the optimizer_class
        batch_size : int
            size of the data batches (default: 128)
        data : np.ndarray
            train data set. If data is passed then dataloader can remain empty (default: None)
        data_eval : np.ndarray
            evaluation data set. If data_eval is passed then evalloader can remain empty (default: None)
        dataloader : torch.utils.data.DataLoader
            dataloader to be used for training (default: default=None)
        evalloader : torch.utils.data.DataLoader
            dataloader to be used for evaluation, early stopping and learning rate scheduling if scheduler=torch.optim.lr_scheduler.ReduceLROnPlateau (default: None)
        optimizer_class : torch.optim.Optimizer
            optimizer to be used (default: torch.optim.Adam)
        loss_fn : torch.nn.modules.loss._Loss
            loss function to be used for reconstruction (default: torch.nn.MSELoss())
        patience : int
            patience parameter for EarlyStopping (default: 5)
        scheduler : torch.optim.lr_scheduler
            learning rate scheduler that should be used.
            If torch.optim.lr_scheduler.ReduceLROnPlateau is used then the behaviour is matched by providing the validation_loss calculated based on samples from evalloader (default: None)
        scheduler_params : dict
            dictionary of the parameters of the scheduler object (default: None)
        device : torch.device
            device to be trained on (default: torch.device('cpu'))
        model_path : str
            if specified will save the trained model to the location. If evalloader is used, then only the best model w.r.t. evaluation loss is saved (default: None)
        print_step : int
            specifies how often the losses are printed. If 0, no prints will occur (default: 0)

        Returns
        -------
        self : FlexibleAutoencoder
            this instance of the FlexibleAutoencoder

        Raises
        ----------
        ValueError: data cannot be None if dataloader is None
        ValueError: evalloader cannot be None if scheduler=torch.optim.lr_scheduler.ReduceLROnPlateau
        """
        if dataloader is None:
            if data is None:
                raise ValueError("data must be specified if dataloader is None")
            dataloader = get_dataloader(data, batch_size, True)
        # evalloader has priority over data_eval
        if evalloader is None:
            if data_eval is not None:
                evalloader = get_dataloader(data_eval, batch_size, False)
        params_dict = {'params': self.parameters(), 'lr': lr}
        optimizer = optimizer_class(**params_dict)

        early_stopping = EarlyStopping(patience=patience)
        if scheduler is not None:
            scheduler = scheduler(optimizer=optimizer, **scheduler_params)
            # Depending on the scheduler type we need a different step function call.
            if isinstance(scheduler, torch.optim.lr_scheduler.ReduceLROnPlateau):
                eval_step_scheduler = True
                if evalloader is None:
                    raise ValueError(
                        "scheduler=torch.optim.lr_scheduler.ReduceLROnPlateau, but evalloader is None. Specify evalloader such that validation loss can be computed.")
            else:
                eval_step_scheduler = False
        best_loss = np.inf
        # training loop
        for epoch_i in range(n_epochs):
            self.train()
            for batch in dataloader:
                loss = self.loss(batch, loss_fn, device)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            if print_step > 0 and ((epoch_i - 1) % print_step == 0 or epoch_i == (n_epochs - 1)):
                print(f"Epoch {epoch_i}/{n_epochs - 1} - Batch Reconstruction loss: {loss.item():.6f}")

            if scheduler is not None and not eval_step_scheduler:
                scheduler.step()
            # Evaluate autoencoder
            if evalloader is not None:
                # self.evaluate calls self.eval()
                val_loss = self.evaluate(dataloader=evalloader, loss_fn=loss_fn, device=device)
                if print_step > 0 and ((epoch_i - 1) % print_step == 0 or epoch_i == (n_epochs - 1)):
                    print(f"Epoch {epoch_i} EVAL loss total: {val_loss.item():.6f}")
                early_stopping(val_loss)
                if val_loss < best_loss:
                    best_loss = val_loss
                    best_epoch = epoch_i
                    # Save best model
                    if model_path is not None:
                        torch.save(self.state_dict(), model_path)

                if early_stopping.early_stop:
                    if print_step > 0:
                        print(f"Stop training at epoch {best_epoch}")
                        print(f"Best Loss: {best_loss:.6f}, Last Loss: {val_loss:.6f}")
                    break
                if scheduler is not None and eval_step_scheduler:
                    scheduler.step(val_loss)
        # Save last version of model
        if evalloader is None and model_path is not None:
            torch.save(self.state_dict(), model_path)
        # Autoencoder is now pretrained
        self.fitted = True
        return self
