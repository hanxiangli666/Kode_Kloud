"""
Set the optimizer to only update the parameters on the final layer in classifier. 
将优化器设置为仅更新分类器最后一层的参数。

Create a `ExponentialLR` scheduler decays the learning rate of the optimizer by 0.1 every epoch.
创建 `ExponentialLR` 调度器，每个 epoch 将优化器的学习率衰减 0.1 倍。
"""
from freeze_mobilenet_v3 import model
# Import module | 导入模块
import torch.nn as nn
import torch.optim as optim

# Create Loss function | 创建损失函数
criterion = nn.CrossEntropyLoss()
# Create Optimizer | 创建优化器
optimizer = optim.SGD(model.classifier[-1].parameters(), lr=0.001, momentum=0.9)
# Create Scheduler | 创建调度器
scheduler = optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.1)
