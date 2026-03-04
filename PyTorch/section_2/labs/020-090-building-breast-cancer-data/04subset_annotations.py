"""
Create 3 CSV files (`training_data.csv`, `validation_data.csv`, and `testing_data.csv`) using Pandas. 

Use the indices from the split data to map the `image_path` and `label` from the `initial_dataset` and use these as columns.
使用Pandas创建3个CSV文件（`training_data.csv`、`validation_data.csv`和`testing_data.csv`）。

利用分割数据的索引从`initial_dataset`中映射出`image_path`和`label`，并将它们用作列。
"""
import os
from initial_dataset import initial_dataset
from split_data import train_dataset, val_dataset, test_dataset
import pandas as pd

# Get the script directory for saving CSV files
script_dir = os.path.dirname(os.path.realpath(__file__))

############ Training
data = []
# For each index in the training dataset indices
for idx in train_dataset.indices:
    # Extract the file_path and the label from the initial dataset 
    image_path = initial_dataset.image_labels['file_path'].loc[idx]
    label = initial_dataset.image_labels['label'].loc[idx]
    # Append path and label 
    data.append({"file_path": image_path, "label": label})

# Create a Dataframe and save as csv file
df = pd.DataFrame(data)
training_file = os.path.join(script_dir, "training_data.csv")
df.to_csv(training_file, index=False)
print(f"训练数据已保存: {training_file}")

############ Validation
data = []
# For each index in the validation dataset indices
for idx in val_dataset.indices:
    # Extract the file_path and the label from the initial dataset 
    image_path = initial_dataset.image_labels['file_path'].loc[idx]
    label = initial_dataset.image_labels['label'].loc[idx]
    # Append path and label 
    data.append({"file_path": image_path, "label": label})

# Create a Dataframe and save as csv file
df = pd.DataFrame(data)
validation_file = os.path.join(script_dir, "validation_data.csv")
df.to_csv(validation_file, index=False)
print(f"验证数据已保存: {validation_file}")

############# Testing
data = []
# For each index in the Testing dataset indices
for idx in test_dataset.indices:
    # Extract the file_path and the label from the initial dataset 
    image_path = initial_dataset.image_labels['file_path'].loc[idx]
    label = initial_dataset.image_labels['label'].loc[idx]
    # Append path and label 
    data.append({"file_path": image_path, "label": label})

# Create a Dataframe and save as csv file
df = pd.DataFrame(data)
testing_file = os.path.join(script_dir, "testing_data.csv")
df.to_csv(testing_file, index=False)
print(f"测试数据已保存: {testing_file}")
