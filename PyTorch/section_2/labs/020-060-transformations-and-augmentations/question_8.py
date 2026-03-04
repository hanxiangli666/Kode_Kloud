""""
Apply a pipeline to a Dataset. 

The pipeline will have 2 steps. 
1. The first step is to transform an image into a tensor. 
2. The second step is to normalize an image using 0.5 for all mean and standard deviation values for RGB channels. 

Create a dataset from the MNIST preloaded dataset and apply pipeline to the dataset.

Use version 1 of the transforms API.
将管道应用于数据集。

该管道包含两个步骤。
1. 第一步是将图像转换为张量。
2. 第二步是使用RGB通道的所有均值和标准差都为0.5的值对图像进行归一化。

从预加载的MNIST数据集中创建一个数据集，并将管道应用于该数据集。

使用第1版的变换API。
"""
import torchvision.transforms as transforms
from torchvision import datasets

# Create the pipeline transform
transform = transforms.Compose([
    transforms.ToTensor,
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

# Create the dataset 
mnist_ds = datasets.MNIST(root='mnist', train=False, download=True, transform=transform)
