"""
Our dataset named cd_dataset that we created in the previous question has 2 available attributes availale to describe our dataset.

Please print the values as strings for each attribute.
我们在上一个问题中创建的名为cd_dataset的数据集有2个可用属性来描述该数据集。

请将每个属性的值以字符串形式打印出来。
"""
from question_3 import cd_dataset

# Annotations attribute
print(f"Annotations data: \n{cd_dataset.annotations}") 
# Class list attribute
print(f"Classes: {cd_dataset.classes}")


