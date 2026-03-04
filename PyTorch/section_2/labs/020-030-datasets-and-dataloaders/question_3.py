"""
This code is a pre-requisite for questions 3-5.

Create a custom dataset class called CatDogDataset.

Fix the methods in the code needed for the Dataset class for our custom dataset.

Finally create a new dataset called cd_dataset. The annotations file is already set as well as the class list.
此代码是问题3-5的先决条件。

创建一个名为CatDogDataset的自定义数据集类。

修复该代码中数据集类所需的方法，以适用于我们的自定义数据集。

最后，创建一个名为cd_dataset的新数据集。标注文件和类别列表已设置好。
"""
import os
import pandas as pd
from PIL import Image
from torchvision import transforms
# Import dataset here
from torch.utils.data import Dataset


# Define our custom Dataset Class
class CatDogDataset(Dataset):
    # Set the methods for Dataset Class
    def __init__(self, annotations_file, class_list):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        annotations_file_path = os.path.join(script_dir, annotations_file)
        self.df = pd.read_csv(annotations_file_path)
        self.class_list = class_list
        self.script_dir = script_dir
        
        # 添加属性别名以满足后续任务需求
        self.annotations = self.df
        self.classes = self.class_list

    def __len__(self):
        return self.df.shape[0]

    def __getitem__(self, index):
        # 修复路径：相对于脚本目录而不是当前工作目录
        img_relative_path = self.df.file_path[index]
        img_full_path = os.path.join(self.script_dir, img_relative_path)
        
        image = Image.open(img_full_path)
        img_url = img_full_path
        # Images must be tensors. Ignore transformations for now.
        convert_tensor = transforms.ToTensor()
        image = convert_tensor(image)
        label = self.class_list.index(self.df.label[index])

        return image, label, img_url


# Create a custom dataset called cd_dataset
cd_dataset = CatDogDataset(annotations_file='labels.csv', class_list=['cat', 'dog'])

# Display the dataset
print(f"Dataset created: {cd_dataset}")
print(f"Dataset size: {len(cd_dataset)}")
print(f"First sample: {cd_dataset[0]}")



