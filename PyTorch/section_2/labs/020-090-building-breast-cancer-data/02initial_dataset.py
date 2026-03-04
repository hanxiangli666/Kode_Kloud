"""
Create a custom PyTorch Dataset called initial_dataset that contains the initial data from our annotations file full_image_data.csv. 

Once again we will use Pandas to read in our annotations file. 

We will then return each index with image_path and label.
创建一个名为initial_dataset的自定义PyTorch数据集，该数据集包含来自我们的标注文件full_image_data.csv的初始数据。

我们将再次使用Pandas来读取标注文件。

然后，我们将返回每个索引对应的image_path（图像路径）和label（标签）。
"""
import os
import pandas as pd
# Import Dataset from torch data utils
from torch.utils.data import Dataset


class BreastCancerDataset(Dataset):
    def __init__(self, annotations_file):
        # Handle both absolute and relative paths
        if not os.path.isabs(annotations_file):
            script_dir = os.path.dirname(os.path.realpath(__file__))
            annotations_file = os.path.join(script_dir, annotations_file)
        self.image_labels = pd.read_csv(annotations_file)

    def __len__(self):
        return len(self.image_labels)

    def __getitem__(self, idx):
        image_path = self.image_labels.iloc[idx, 0]
        label = self.image_labels.iloc[idx, 1]
        # Return image path and label
        return image_path, label

# Create the initial dataset
initial_dataset = BreastCancerDataset(annotations_file='full_image_data.csv')

# Print dataset info
if __name__ == "__main__":
    print(f"数据集大小: {len(initial_dataset)}")
    sample_path, sample_label = initial_dataset[0]
    print(f"第一条样本 - 路径: {sample_path}, 标签: {sample_label}")
