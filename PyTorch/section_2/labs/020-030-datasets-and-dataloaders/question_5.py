"""
Create a dataloader from our dataset named cd_dataset called cd_dataloader and then iterate through a batch and print the features and labels shape. 

When creating the dataloader, set the size of the batch to 4.  
从名为cd_dataset的数据集创建一个名为cd_dataloader的数据加载器，然后遍历一个批次并打印特征和标签的形状。
创建数据加载器时，将批次大小设置为4。
"""
from question_3 import cd_dataset
# Import dataloader utility here
from torch.utils.data import DataLoader

# Create the dataloader called cd_dataloader and set size to 4. 
cd_dataloader = DataLoader(dataset=cd_dataset, batch_size=4, shuffle=True)

# Iterate through this dataloader like we did above
features, labels, urls = next(iter(cd_dataloader))

# Print the batch size and the number of labels
print(f"Features batch shape: {features.shape}")
print(f"Labels batch size shape: {labels.shape}")
