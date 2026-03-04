"""
Create a transform pipeline. 

The first step of the pipeline is to resize the image to 100 by 100 pixels. 

The second step of the pipeline is to randomly horizontally flip the image 50% of the time. 

The third and final step is to randomly distort the image by changing the contrast of the image with a minimum of .7 and a maximum of 1.2. 

Apply the transformation using v2 of the API.
创建一个转换管道。

管道的第一步是将图像调整为100×100像素。

管道的第二步是有50%的概率随机水平翻转图像。

第三步也是最后一步是通过改变图像的对比度来随机扭曲图像，对比度的最小值为0.7，最大值为1.2。

使用API的v2版本应用该转换。
"""
import os
from torchvision.transforms import v2
from PIL import Image

# Get the directory where this script is located / 获取脚本所在目录
script_dir = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(script_dir, 'images/dog/dog-5.jpg')

# load the image into memory / 将图像加载到内存中
image = Image.open(image_path)

# Create the Pipeline transform
pipeline = v2.Compose([
    v2.Resize((100, 100)),
    v2.RandomHorizontalFlip(0.5),
    v2.ColorJitter(contrast=(0.7, 1.2))
])

# Apply the pipeline
pipeline_image = pipeline(image)
