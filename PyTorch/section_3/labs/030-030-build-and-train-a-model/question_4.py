"""
Define a loss function. 
定义损失函数。

Import the module and create an instance of a loss function called “criterion” using Cross Entropy Loss.
导入模块，并使用交叉熵损失创建一个名为“criterion”的损失函数实例。

"""
# Import the module as nn | 以 nn 名称导入模块
import torch.nn as nn

# Create a loss function for binary classification with sigmoid output | 创建二分类损失函数（适用于 sigmoid 输出）
criterion = nn.BCELoss()  # Binary Cross Entropy Loss for sigmoid outputs / 用于 sigmoid 输出的二元交叉熵损失
