"""
Using v1 of the transforms API, resize the following image to 250 pixels by 300 pixels. 

Use the pillow library to first load the image.
使用transforms API的v1版本，将以下图像调整为250像素×300像素。

首先使用pillow库加载该图像。
"""
import os
from torchvision import transforms
from PIL import Image

# Get the directory where this script is located / 获取脚本所在目录
script_dir = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(script_dir, 'images/dog/dog-1.jpg')

# Load the image into memory / 将图像加载到内存中
image = Image.open(image_path)

# Create the resize transform
resize_transform = transforms.Resize((250, 300))

# Apply the transform
resized_image = resize_transform(image)
