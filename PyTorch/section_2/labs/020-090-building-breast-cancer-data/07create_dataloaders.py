"""
Create PyTorch DataLoaders for the train_dataset and the  val_dataset. 

This will define how the data is passed to the model during training and is the last step before you train the model. 

The train_loader should take in the train_dataset with a batch size of 64 and should shuffle. 

The val_loader should take the val_dataset with a batch size of 32 and should not shuffle. 
为训练数据集（train_dataset）和验证数据集（val_dataset）创建PyTorch数据加载器（DataLoaders）。

这将定义在训练过程中数据如何传递给模型，并且是训练模型前的最后一步。

训练加载器（train_loader）应接收训练数据集，批处理大小设为64，且需要打乱数据顺序。

验证加载器（val_loader）应接收验证数据集，批处理大小设为32，且不需要打乱数据顺序。
"""
from create_datasets import train_dataset, val_dataset
# Import DataLoader
from torch.utils.data import DataLoader

# Create the training DataLoader
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

# Create the Validation DataLoader
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# Verify DataLoaders / 验证数据加载器
if __name__ == "__main__":
    print(f"训练DataLoader - 批次数量: {len(train_loader)}")
    print(f"验证DataLoader - 批次数量: {len(val_loader)}")
    
    # Get a sample batch / 获取一个样本批次
    sample_batch, sample_labels = next(iter(train_loader))
    print(f"样本批次形状: {sample_batch.shape}")  # [batch_size, channels, height, width]
    print(f"样本标签形状: {sample_labels.shape}")
    print(f"样本标签: {sample_labels[:5]}")  # 打印前5个标签
