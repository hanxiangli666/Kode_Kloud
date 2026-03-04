"""
Using the custom PyTorch Dataset Class provided, create a training dataset called train_dataset and a validation dataset called val_dataset. 

For each use the proper transformations and the proper annotations file. 

Also be sure to create the label encoding for our 2 labels (benign and malignant) and pass the label_encoder as the target_transform.
使用所提供的自定义PyTorch数据集类，创建一个名为train_dataset的训练数据集和一个名为val_dataset的验证数据集。

为每个数据集使用适当的变换和适当的标注文件。

同时，确保为我们的两个标签（良性和恶性）创建标签编码，并将label_encoder作为target_transform传入。
"""
from create_transformations import train_transform, val_transform
import os
import pandas as pd
from PIL import Image
from torch.utils.data import Dataset

# Get the directory where this script is located / 获取脚本所在目录
script_dir = os.path.dirname(os.path.realpath(__file__))

# Navigate up to PyTorch root directory / 向上导航到PyTorch根目录（向上3级）
pytorch_root = os.path.abspath(os.path.join(script_dir, '..', '..', '..'))
data_dir = os.path.join(pytorch_root, 'data')


class CustomImageBreastCancerDataSet(Dataset):
    def __init__(self, annotations_file, image_dir, transform, target_transform):
        self.image_labels = pd.read_csv(annotations_file)
        self.image_dir = image_dir
        self.transform = transform
        self.target_transform = lambda y: target_transform[y]

    def __len__(self):
        return len(self.image_labels)

    def __getitem__(self, idx):
        # 获取CSV中的完整路径（来自full_image_data.csv）
        image_path = self.image_labels.iloc[idx, 0]
        # 如果不是绝对路径，则与image_dir结合
        if not os.path.isabs(image_path):
            image_path = os.path.join(self.image_dir, image_path)
        image = Image.open(image_path)
        label = self.image_labels.iloc[idx, 1]
        image = self.transform(image)
        label = self.target_transform(label)
        
        return image, label


# Label encoding
label_encoding = {'benign': 0, 'malignant': 1}

# Create the Training Dataset / 创建训练数据集
train_dataset = CustomImageBreastCancerDataSet(
    annotations_file=os.path.join(script_dir, 'training_data.csv'), 
    image_dir=data_dir,  # 使用PyTorch根目录的data文件夹
    transform=train_transform, 
    target_transform=label_encoding
)

# Create the Validation Dataset / 创建验证数据集
val_dataset = CustomImageBreastCancerDataSet(
    annotations_file=os.path.join(script_dir, 'validation_data.csv'), 
    image_dir=data_dir,  # 使用PyTorch根目录的data文件夹
    transform=val_transform, 
    target_transform=label_encoding
)

# Print dataset info / 打印数据集信息
if __name__ == "__main__":
    print(f"训练集大小: {len(train_dataset)}")
    print(f"验证集大小: {len(val_dataset)}")
    sample_img, sample_label = train_dataset[0]
    print(f"样本图片形状: {sample_img.shape}, 样本标签: {sample_label}")
