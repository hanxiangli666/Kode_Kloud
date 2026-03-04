"""
Define `train_transform` and `val_transform` pipelines. 

For the `train_transform` we need the following in our pipeline in the following order: 
Resize of 128 x 128 pixels
Set to Grayscale
30 degrees random rotation
50% chance of a random horizontal flip
converted to a tensor
normalized mean (0.485, 0.456, 0.406) and standard deviation (0.229, 0.224, 0.225) for 3 channels

For the `val_transform` we need the following: 
Resize of 128 x 128 pixels
Set to Grayscale
converted to a tensor
normalized mean (0.485, 0.456, 0.406) and standard deviation (0.229, 0.224, 0.225) for 3 channels

Use V2 API
定义`train_transform`和`val_transform`管道。

对于`train_transform`，我们的管道需要按以下顺序包含以下操作：
调整大小为128×128像素
设置为灰度图
30度随机旋转
50%的概率进行随机水平翻转
转换为张量
对3个通道使用均值（0.485, 0.456, 0.406）和标准差（0.229, 0.224, 0.225）进行归一化

对于`val_transform`，我们需要以下操作：
调整大小为128×128像素
设置为灰度图
转换为张量
对3个通道使用均值（0.485, 0.456, 0.406）和标准差（0.229, 0.224, 0.225）进行归一化

使用V2 API
"""
import torch
# Import transforms version 2
from torchvision.transforms import v2

# Train Pipeline
train_transform = v2.Compose([
    v2.Resize((128, 128)),
    v2.Grayscale(num_output_channels=1),
    v2.RandomRotation(degrees=30),
    v2.RandomHorizontalFlip(p=0.5),
    v2.ToImage(), 
    v2.ToDtype(torch.float32, scale=True),
    v2.Normalize(mean=[0.485, 0.456, 0.406], 
                 std=[0.229, 0.224, 0.225])
])

# Validation Pipeline. Hint: Copy
val_transform = v2.Compose([
    v2.Resize((128, 128)),
    v2.Grayscale(num_output_channels=1),
    v2.ToImage(), 
    v2.ToDtype(torch.float32, scale=True),
    v2.Normalize(mean=[0.485, 0.456, 0.406], 
                 std=[0.229, 0.224, 0.225])
])
