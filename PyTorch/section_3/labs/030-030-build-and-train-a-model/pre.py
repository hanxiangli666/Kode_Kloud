"""
Additional code that needs to run to make other code work
让其他代码正常运行所需的附加代码
"""
import torch
from torch.utils.data import Dataset, DataLoader

# Simple learnable dataset | 简单可学习数据集
class SimpleDataset(Dataset):
    def __init__(self, num_samples=100, input_size=(3, 34, 34)):
        self.num_samples = num_samples
        self.input_size = input_size

    def __len__(self):
        return self.num_samples

    def __getitem__(self, idx):
        # Create data with clear patterns | 创建有明确规律的数据
        if idx % 2 == 0:
            # Even index: bright images → label 1 | 偶数索引：亮图像 → 标签1
            image = torch.ones(self.input_size) * 0.8 + torch.randn(self.input_size) * 0.1
            label = 1
        else:
            # Odd index: dark images → label 0 | 奇数索引：暗图像 → 标签0
            image = torch.ones(self.input_size) * 0.2 + torch.randn(self.input_size) * 0.1
            label = 0
        
        # Clamp values to [0, 1] | 限制值在 [0, 1] 范围
        image = torch.clamp(image, 0, 1)
        return image, label

# dataset and dataloader | 数据集和数据加载器
train_dataset = SimpleDataset(num_samples=100, input_size=(3, 34, 34))
train_dataloader = DataLoader(train_dataset, batch_size=16, shuffle=True)
