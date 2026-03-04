"""
Using the cd_dataset dataset created using folder structure in question 6, print the classes and the classes to index dictionary for our dataset created by folder structure.
使用在问题6中通过文件夹结构创建的cd_dataset数据集，打印出我们通过文件夹结构创建的数据集的类别以及类别到索引的字典。

"""
from question_6 import cd_dataset

# Print the classes
print(f"Classes: {cd_dataset.classes}")
# Print the classes to indexes
print(f"Classes to indexes: {cd_dataset.class_to_idx}")
