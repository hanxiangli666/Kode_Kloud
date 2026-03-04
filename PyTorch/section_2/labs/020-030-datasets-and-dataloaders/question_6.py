"""
Create a new dataset called cd_dataset using the folder structure as classes. Use the images directory.
使用图像目录，按照文件夹结构作为类别，创建一个名为cd_dataset的新数据集。
"""
# Import the module needed
import os
import torchvision

# Get the directory where this script is located / 获取脚本所在目录
script_dir = os.path.dirname(os.path.realpath(__file__))
images_dir = os.path.join(script_dir, 'images')

# Ignore this line
transformations = torchvision.transforms.Compose([torchvision.transforms.ToTensor()])

# Create a dataset using the images folder called cd_dataset.
cd_dataset = torchvision.datasets.ImageFolder(root=images_dir, transform=transformations)
