"""
Import the modules necessary to create a dataset and to use preloaded image datasets. 

Create a dataset using the "MNIST" preloaded dataset. 

Download the dataset to a folder called "mnist".
导入创建数据集和使用预加载图像数据集所需的模块。

使用“MNIST”预加载数据集创建一个数据集。

将该数据集下载到名为“mnist”的文件夹中。
"""
# Import the modules
from torch.utils.data import DataLoader
import torchvision.datasets
from torchvision.transforms import ToTensor

# Create a dataset using the preloaded MNIST dataset. 
# Download it to a folder called "mnist"
mnist_dataset = torchvision.datasets.MNIST(
    root='mnist',
    train=True,
    download=True,
    transform=ToTensor()
)
