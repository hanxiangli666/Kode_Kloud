"""
Load the `mobilenet_v3_large` pre-trained model from `v0.10.0` of the PyTorch vision github repo. 
从 PyTorch vision GitHub 仓库 `v0.10.0` 加载 `mobilenet_v3_large` 预训练模型。

Be sure to load the pre-trained parameters.
请确保加载预训练参数。

"""
# import modules | 导入模块
from torchvision import models

# Load Model from the hub | 从模型仓库加载模型
model = models.mobilenet_v3_large(pretrained=True)
