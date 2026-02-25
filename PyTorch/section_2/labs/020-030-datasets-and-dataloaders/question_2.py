"""
Import the modules necessary to create a dataset and to use preloaded image datasets. 

Create a dataset using the "MNIST" preloaded dataset. 

Download the dataset to a folder called "mnist".
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
