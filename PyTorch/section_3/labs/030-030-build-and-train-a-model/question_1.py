"""
Create a Class to build a Neural Network in a PyTorch manner. 
以 PyTorch 的方式创建一个用于构建神经网络的类。

Begin by importing the Neural Network module from PyTorch and name your Class “Neural Network”. 
首先从 PyTorch 导入神经网络模块，并将你的类命名为“Neural Network”。

Then define your layers as follows: 1) A 2D convolutional layer, 2) a 2D max pooling layer and 3) a fully connected layer. 
然后按如下方式定义层：1）二维卷积层，2）二维最大池化层，3）全连接层。

Once layers have been defined, then define the flow through the layers as follows: 1) pass through conv layer with ReLU activation, then apply max pooling, 2) flatten the output from the convolutional layers, and then 3) pass through fully connected layer with sigmoid.
定义好层之后，再按如下方式定义前向流程：1）通过带 ReLU 激活的卷积层并进行最大池化，2）将卷积层输出展平，3）通过带 sigmoid 的全连接层。

"""
import torch
# Import the nn module | 导入 nn 模块
import torch.nn as nn 
import torch.nn.functional as F

# Create a Neural Network that inherits the Neural Network module | 创建继承 nn.Module 的神经网络
class NeuralNetwork(nn.Module):
    # Function for defining layers | 定义网络层的函数
    def __init__(self):
        # Initialize superclass for automatic parameter initialization | 初始化父类以自动初始化参数
        super(NeuralNetwork, self).__init__()
        # Define a 2D convolutional layer | 定义二维卷积层
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3)
        # Define a 2D max pooling layer | 定义二维最大池化层
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        # Define a fully connected layer | 定义全连接层
        self.fc1 = nn.Linear(16 * 16 * 16, 1)

    # Function for defining flow through the network. | 定义网络前向传播流程的函数
    def forward(self, x):
        # Pass through conv layer with ReLU activation, then apply max pooling | 通过卷积层+ReLU后进行最大池化
        x = self.pool(F.relu(self.conv1(x)))
        # Flatten the output from the convolutional layers | 展平卷积层输出
        x = x.view(-1, 16 * 16 * 16)
        # Pass through fully connected layer with sigmoid activation | 通过全连接层并应用 Sigmoid 激活
        x = torch.sigmoid(self.fc1(x))
        
        return x
    
