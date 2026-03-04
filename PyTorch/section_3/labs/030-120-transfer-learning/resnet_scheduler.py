"""
Create StepLR scheduler that reduces the learning rate by 0.1 every 2 epochs
创建 StepLR 调度器，每 2 个 epoch 将学习率减少 0.1 倍
"""
from modify_resnet_output import model
# Import module | 导入模块
import torch.nn as nn
import torch.optim as optim

# Create Loss function | 创建损失函数
criterion = nn.CrossEntropyLoss()
# Create Optimizer | 创建优化器
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
# Create Scheduler | 创建调度器
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=2, gamma=0.1)
