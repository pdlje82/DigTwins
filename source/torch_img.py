import torch
import logging
from pathlib import Path
import numpy as np
from torch.utils.tensorboard import SummaryWriter

logger = logging.getLogger(__name__)


class TorchOrthoImage:
    def __init__(self, image, expected_channels=3):
        self.log_dir = Path('./logs').resolve()
        self.image = image
        self.expected_channels = expected_channels
        self.tensor_image = self._to_tensor()
        self._check_and_fix_channels()
        self.writer = SummaryWriter(self.log_dir)
        self._log_tensorboard()

        logger.info(self.log_dir)

    def _to_tensor(self):
        """
        Convert the image to a PyTorch tensor.
        """
        if self.image.dtype != np.uint8:
            logger.warning(f"Image type {self.image.dtype} not supported, converting to uint8.")

        tensor_img = torch.tensor(self.image, dtype=torch.uint8)
        self._log_tensor_size(tensor_img)
        return tensor_img

    def _check_and_fix_channels(self):
        """
        Check if the tensor has the correct number of channels.
        If the channels are not first, rearrange the tensor to have channels first.
        Raises an exception if the number of channels is incorrect.
        """
        if len(self.tensor_image.shape) != 3:
            raise ValueError("Image tensor must have three dimensions (channels, height, width).")

        # Check if channels are first
        if self.tensor_image.shape[0] == self.expected_channels:
            # Channels are already first
            return
        elif self.tensor_image.shape[2] == self.expected_channels:
            # Channels are last, permute to (channels, height, width) in-place
            self.tensor_image = self.tensor_image.permute(2, 0, 1)
        else:
            raise ValueError(f"Expected {self.expected_channels} channels, but got {self.tensor_image.shape[0]} and {self.tensor_image.shape[2]}.")

    def _log_tensor_size(self, tensor_img):
        """
        Log the size of the tensor in megabytes.
        """
        tensor_size_bytes = tensor_img.numel() * tensor_img.element_size()
        tensor_size_mb = tensor_size_bytes / (1024 * 1024)  # Convert bytes to megabytes
        logger.info(f"Tensor is {tensor_size_mb:.2f} MB in size.")


    def _log_tensorboard(self):
        """
        Log the tensor to TensorBoard.
        """
        self.writer.add_image('Image', self.tensor_image, 0)
        self.writer.flush()


