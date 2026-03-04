"""
Normalize the image and then randomly resize it. 

The mean values for the RGB channels should all be 0.5 and the standard deviation should also be set to 0.5. 

The minimum size of the image should be 50 pixels and the maximum size of the image should be 300 pixels. 

Use v2 of the API.
对图像进行归一化处理，然后随机调整其大小。

RGB通道的均值都应设为0.5，标准差也应设为0.5。

图像的最小尺寸应为50像素，最大尺寸应为300像素。

使用API的v2版本。
"""
import os
from torchvision.transforms import v2
from PIL import Image

# Get the directory where this script is located / 获取脚本所在目录
script_dir = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(script_dir, 'images/dog/dog-1.jpg')

# Load the image to memory / 将图像加载到内存中
img = Image.open(image_path)

# Normalize() does not support PIL images.
# 先转为图像张量，再转为浮点型，然后才能归一化
tensor_transform = v2.ToImage()
tensor_img = tensor_transform(img)

# Convert to float tensor / 转换为浮点型张量
import torch
float_transform = v2.ToDtype(torch.float32, scale=True)
float_img = float_transform(tensor_img)

# Normalize the image / 归一化图像（RGB三个通道都设为0.5）
normalize_transform = v2.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]) 
normalize_img = normalize_transform(float_img)

# Randomly resize the image
rand_resize_transform = v2.RandomResizedCrop(size=(100, 100), scale=(50/300, 1.0))
rand_resize_img = rand_resize_transform(normalize_img)
