"""
Load the resnet18 model with pre-trained weights.
加载带预训练权重的 resnet18 模型。

Use the DEFAULT class weights.
使用 DEFAULT 类别权重。
"""
# import module | 导入模块
from torchvision import models

# load the resnet18 model from torchvision with default weights | 从 torchvision 加载带默认权重的 resnet18
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
