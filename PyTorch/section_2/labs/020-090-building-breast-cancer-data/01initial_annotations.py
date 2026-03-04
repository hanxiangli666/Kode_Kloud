"""
Build an annotations file to build our initial dataset. 

Using Pandas, create a CSV file named full_image_data.csv that contains 2 columns: file_path and label. 

file_path is the path to the image and label being the label to classify the image. 

The label is in the path of the image.
创建一个标注文件来构建我们的初始数据集。

使用Pandas创建一个名为full_image_data.csv的CSV文件，该文件包含两列：file_path（文件路径）和label（标签）。

file_path是图像的路径，label是用于对图像进行分类的标签。

标签位于图像的路径中。
"""
import os
import glob
# Import Pandas
import pandas as pd

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.realpath(__file__))
# Navigate up to PyTorch root directory (3 levels up)
pytorch_root = os.path.abspath(os.path.join(script_dir, '..', '..', '..'))
data_dir = os.path.join(pytorch_root, 'data')

data = []

for file_path in glob.glob(os.path.join(data_dir, "*", "*jpg")):
    # Extract the class label from the file path
    label = os.path.basename(os.path.dirname(file_path))
    # Append file path and label in a dictionary to data
    data.append({"file_path": file_path, "label": label})

# Create a Dataframe from the data list 
df = pd.DataFrame(data)
# Save the Dataframe as a CSV file in the script directory
output_file = os.path.join(script_dir, "full_image_data.csv")
df.to_csv(output_file, index=False)
print(f"生成的CSV文件保存在: {output_file}")
print(f"共找到 {len(data)} 张图片")
