"""
With v2, first transform the image into a tensor. Second, randomly crop the image at 50 x 200 pixels.
在v2版本中，首先将图像转换为张量。其次，对图像进行50×200像素的随机裁剪。
"""
import os
from torchvision.transforms import v2
from PIL import Image

# Get the directory where this script is located / 获取脚本所在目录
script_dir = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(script_dir, 'images/cat/cat-3.jpg')

# Load image into memory / 将图像加载到内存中
image = Image.open(image_path)

# Transform the image to a tensor and apply it / 将图像转换为张量并应用
tensor_transform = v2.ToImage()
tensor_image = tensor_transform(image)

# Transform the tensor image by random crop and apply it
random_crop_transform = v2.RandomCrop((50, 200))
random_crop_image = random_crop_transform(tensor_image)
