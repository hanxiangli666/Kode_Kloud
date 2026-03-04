"""
Define an optimizer. 
定义优化器。

Import the module for optimizers and create using the Adam optimizer using our model weights and a learning rate of 0.001. 
导入优化器模块，并使用模型权重和 0.001 学习率创建 Adam 优化器。

"""
from question_2 import model
# Import the module | 导入模块
import torch.optim as optim

# Create the optimizer and pass in the model weights and an learning rate of 0.001 | 创建优化器并传入模型权重与 0.001 学习率
optimizer = optim.Adam(model.parameters(), lr=0.001)
