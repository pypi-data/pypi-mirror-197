from enum import Enum


class Device(Enum):
    MPS = 'mps'
    CPU = 'cpu'
    CUDA = 'cuda'
    CUDNN = 'cudnn'
    MKL = 'mkl'
    MKLDNN = 'mkldnn'
    OPENMP = 'openmp'
    QUANTIZED = 'quantized'
