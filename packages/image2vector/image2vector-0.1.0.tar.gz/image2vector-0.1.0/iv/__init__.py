from typing import List, Union
from pathlib import Path
from io import BytesIO
import torch
import numpy
from PIL import Image
from numpy import ndarray
from torch import Tensor
from torch import device as TorchDevice
from torchvision import transforms
from iv.cirtorch.networks.imageretrievalnet import ImageRetrievalNet
from iv.schemas import Device


__version__ = '0.1.0'
VERSION = __version__


preprocess = transforms.Compose([
    transforms.Resize(224),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


class ResNet:
    def __init__(
        self,
        weight_file: Union[Path, str],
        device: Union[Device, str] = Device.CPU
    ) -> None:
        assert isinstance(device, (Device, str))
        self.device = TorchDevice(
            device.value if isinstance(device, Device) else device)

        if isinstance(weight_file, Path):
            weight_file = str(weight_file)

        self.weight_file = weight_file

        self.load_network()
        # self.init_transform()

    def load_network(self):
        state: dict = torch.load(self.weight_file)

        state['state_dict']['whiten.weight'] = state['state_dict']['whiten.weight'][0::4, ::]
        state['state_dict']['whiten.bias'] = state['state_dict']['whiten.bias'][0::4]

        network: ImageRetrievalNet = ImageRetrievalNet()
        network.load_state_dict(state['state_dict'])
        network.eval()
        network.to(self.device)
        self.network = network

    def images_to_vectors(self, images: Tensor) -> Tensor:
        with torch.no_grad():
            _img_tensor = images.to(self.device)
            features = self.network(_img_tensor)
            vectors = torch.transpose(features, 0, 1)
            return vectors

    def gen_vector(
        self,
        image: Union[Image.Image, ndarray, Path, str, bytes],
        batch_size: int = 1,
        num_workers: int = 0
    ) -> List[float]:
        if isinstance(image, bytes):
            image_file_like = BytesIO(image)
            image = Image.open(image_file_like).convert('RGB')

        if isinstance(image, Image.Image):
            image = image.convert('RGB')

        if isinstance(image, Path) or isinstance(image, str):
            image = Image.open(str(image)).convert('RGB')

        if isinstance(image, ndarray):
            image = Image.fromarray(image).convert('RGB')

        assert isinstance(image, Image.Image)

        batch_size = 1

        preprocessed_image: torch.Tensor = preprocess(image)
        unsqueezed_image = preprocessed_image.unsqueeze(0)

        _images = torch.cat([unsqueezed_image]*batch_size, dim=0)

        vectors = self.images_to_vectors(_images)

        return vectors.squeeze(0).tolist()

    def gen_vectors(
        self,
        images: List[Union[Image.Image, ndarray, Path, str, bytes]],
        batch_size: int = 1,
        num_workers: int = 0
    ) -> List[List[float]]:

        assert isinstance(images, List)
        assert len(images) > 0

        for index, image in enumerate(images):
            if isinstance(image, bytes):
                image_file_like = BytesIO(image)
                image = Image.open(image_file_like).convert('RGB')
                images[index] = image

            if isinstance(image, Image.Image):
                image = image.convert('RGB')
                images[index] = image

            if isinstance(image, Path) or isinstance(image, str):
                image = Image.open(str(image)).convert('RGB')
                images[index] = image

            if isinstance(image, ndarray):
                image = Image.fromarray(image).convert('RGB')
                images[index] = image

        assert isinstance(images[0], Image.Image)

        for index, image in enumerate(images):
            preprocessed_image: torch.Tensor = preprocess(image)
            unsqueezed_image = preprocessed_image.unsqueeze(0)
            images[index] = unsqueezed_image

        _images = torch.cat(images, dim=0)

        vectors = self.images_to_vectors(_images)

        return vectors.tolist()


def l2(vector1: List[float], vector2: List[float]) -> float:
    vector1 = numpy.array(vector1)
    vector2 = numpy.array(vector2)
    return float(numpy.sqrt(numpy.sum(numpy.square(vector1 - vector2))))
