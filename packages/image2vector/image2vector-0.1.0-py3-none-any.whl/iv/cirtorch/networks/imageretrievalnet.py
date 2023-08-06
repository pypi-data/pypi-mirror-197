import torch.nn as nn
from torch import Tensor
from iv.cirtorch.layers.pooling import MAC, SPoC, GeM, GeMmp, RMAC
from iv.cirtorch.layers.normalization import L2N
from iv.cirtorch.layers.pooling import GeM
import torchvision.models as models


class ImageRetrievalNet(nn.Module):

    def __init__(self, dim: int = 512):
        super(ImageRetrievalNet, self).__init__()
        resnet50_model = models.resnet50()
        features = list(resnet50_model.children())[:-2]
        self.features = nn.Sequential(*features)

        self.lwhiten = None
        self.pool = GeM()
        self.whiten = nn.Linear(2048, dim, bias=True)
        self.norm = L2N()

    def forward(self, x: Tensor):
        o: Tensor = self.features(x)

        # features -> pool -> norm

        pooled_t: Tensor = self.pool(o)
        normed_t: Tensor = self.norm(pooled_t)
        o: Tensor = normed_t.squeeze(-1).squeeze(-1)

        # 启用白化，则: pooled features -> whiten -> norm
        if self.whiten is not None:
            whitened_t = self.whiten(o)
            normed_t: Tensor = self.norm(whitened_t)
            o = normed_t

        # 使每个图像为Dx1列向量(如果有许多图像，则为DxN)
        return o.permute(1, 0)


def init_network() -> ImageRetrievalNet:
    return ImageRetrievalNet()
