"""
Set the last layer in the classifier layer to use 2 classes.
将分类器中的最后一层设置为 2 个类别输出。

Freeze all layers.
冻结所有层。

Unfreeze only the final layer.
仅解冻最后一层。
"""
from load_mobilenet_v3 import model
# import module | 导入模块
import torch.nn as nn

# Modify last layer of the model for 2 classes | 将模型最后一层改为 2 类输出
model.classifier[-1] = nn.Linear(1280, 2)

# Freeze all layers | 冻结所有层
for param in model.parameters():
    param.requires_grad = False

# Unfreeze last layer | 解冻最后一层
for param in model.classifier[-1].parameters():
    param.requires_grad = True
