"""
Modify the last layer to output 2 classes
将最后一层修改为输出 2 个类别
"""
from load_resnet_model import model
# Import module | 导入模块
import torch.nn as nn

# Set classes in output layer to 2 | 将输出层的类别设置为 2
model.fc = nn.Linear(512, 2)

