"""
This file is used to create Datasets, DataLoaders and Transformations we already created in the Build Breast Cancer data Lab
该文件用于创建我们在“构建乳腺癌数据”实验中已实现的数据集、数据加载器和数据变换。
"""
import pandas as pd
import os
import torch
from torch.utils.data import Dataset
from PIL import Image
from torchvision.transforms import v2
from torch.utils.data import DataLoader


# Dataset Class | 数据集类
class CustomImageDataset(Dataset):
    def __init__(self, annotations_file, img_dir, transform, target_transform):
        self.img_labels = pd.read_csv(annotations_file)
        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = lambda y: target_transform[y]

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 0])
        image = Image.open(img_path)
        label = self.img_labels.iloc[idx, 1]
        # Transform the image | 图像变换
        image = self.transform(image)
        # Get the label | 获取标签
        label = self.target_transform(label)
        
        return image, label
    

# Label Encoding | 标签编码
label_encoding = {"malignant": 0, "benign": 1}

# Training Transformations | 训练集变换
train_transform = v2.Compose([
    v2.Resize(224),
    v2.RandomRotation(degrees=30),
    v2.RandomHorizontalFlip(p=.5),
    v2.ToImage(), 
    v2.ToDtype(torch.float32, scale=True),
    v2.Normalize(mean=[0.485, 0.456, 0.406], 
                 std=[0.229, 0.224, 0.225])
])

# set current directory | 设置当前目录
work_dir = os.path.dirname(os.path.abspath(__file__))

# Set data directory | 设置数据目录
# Data is located at PyTorch/data/, and script is at PyTorch/section_3/labs/030-120-transfer-learning/
# CSV contains paths like "data/benign/xxx.jpg", so img_dir should point to PyTorch/ directory
# 数据位于 PyTorch/data/，脚本位于 PyTorch/section_3/labs/030-120-transfer-learning/
# CSV 包含类似 "data/benign/xxx.jpg" 的路径，所以 img_dir 应指向 PyTorch/ 目录
data_dir = os.path.join(work_dir, '../../../')

# Training dataset | 训练数据集
train_dataset = CustomImageDataset(
    annotations_file=os.path.join(work_dir, 'training_data.csv'), 
    img_dir=data_dir, 
    transform=train_transform, 
    target_transform=label_encoding
)

# Train DataLoader | 训练数据加载器
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# Validation Transformations | 验证集变换
val_transform = v2.Compose([
    v2.Resize(224),
    v2.ToImage(), 
    v2.ToDtype(torch.float32, scale=True),
    v2.Normalize(mean=[0.485, 0.456, 0.406], 
                 std=[0.229, 0.224, 0.225])
])

# Validation Dataset | 验证数据集
val_dataset = CustomImageDataset(
    annotations_file=os.path.join(work_dir, 'val_data.csv'), 
    img_dir=data_dir, 
    transform=val_transform, 
    target_transform=label_encoding
)

# Validation DataLoader | 验证数据加载器
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)




