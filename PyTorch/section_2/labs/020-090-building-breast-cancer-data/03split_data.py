"""
Split the initial_dataset into training, validation and testing datasets using the function from PyTorch used to randomly split data. 

Call the training data train_dataset, validation data val_dataset and the testing data test_data. 

Use 70% for training, 20% for validation and 10% for testing.
使用PyTorch中用于随机拆分数据的函数，将初始数据集（initial_dataset）拆分为训练数据集、验证数据集和测试数据集。

将训练数据命名为train_dataset，验证数据命名为val_dataset，测试数据命名为test_data。

拆分比例为：70%用于训练，20%用于验证，10%用于测试。
"""
from initial_dataset import initial_dataset
# Import the random split function 
from torch.utils.data import random_split

# Define size of Training data
train_size = int(0.7 * len(initial_dataset))
# Define size of Validation data 
val_size = int(0.2 * len(initial_dataset))
# Finally define the rest as test 
test_size = len(initial_dataset) - train_size - val_size

# Randomly Split the data for train dataset, validation dataset and then test dataset
train_dataset, val_dataset, test_dataset = random_split(initial_dataset, [train_size, val_size, test_size])
