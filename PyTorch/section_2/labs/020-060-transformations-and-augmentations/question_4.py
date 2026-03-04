"""
Using v2 of the transforms API, create a random horizontal flip of the image. 

The probability that the transformation takes place should be 75%.
使用transforms API的v2版本，创建图像的随机水平翻转。

该变换发生的概率应为75%。
"""
import os
from torchvision.transforms import v2
from PIL import Image

# Get the directory where this script is located / 获取脚本所在目录
script_dir = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(script_dir, 'images/dog/dog-2.jpg')

# Load the image to memory / 将图像加载到内存中
image = Image.open(image_path)

# Create the transformation
transform = v2.RandomHorizontalFlip(p=0.75)
# Apply the transformation
rhf_image = transform(image)
