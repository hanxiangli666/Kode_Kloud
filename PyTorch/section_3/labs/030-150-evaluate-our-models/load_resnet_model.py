"""
Using pre-trained models from torchvision, load resnet18 with default Resnet18 weghts.
使用 torchvision 中的预训练模型，加载带默认 Resnet18 权重的 resnet18。

Set output layer to 2 classes.
将输出层设置为 2 个类别。

Load our fine tuned model from a checkpoint.
从检查点加载我们微调后的模型。

Load the model parameters from the checkpoint. 
从检查点加载模型参数。
"""
# Import modules | 导入模块
from pathlib import Path
import torch
import torch.nn as nn
from torchvision import models

# Load the model from torchvision models using default weights | 使用默认权重从 torchvision 加载模型
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

# Set classes in output layer to 2 | 将输出层的类别设置为 2
model.fc = nn.Linear(512, 2)

# Locate latest checkpoint | 定位最新检查点
script_dir = Path(__file__).resolve().parent
workspace_dir = Path.cwd()
transfer_lab_dir = script_dir.parent / "030-120-transfer-learning"

candidate_files = []
for candidate_dir in [script_dir, transfer_lab_dir, workspace_dir]:
	candidate_files.extend(candidate_dir.glob("resnet_*_checkpoint.tar"))

if not candidate_files:
	raise FileNotFoundError(
		"No ResNet checkpoint found. Expected files like resnet_0_checkpoint.tar. "
		"Please run train_resnet.py in 030-120-transfer-learning first."
	)

latest_checkpoint = max(candidate_files, key=lambda p: int(p.stem.split("_")[1]))
print(f"Loading checkpoint: {latest_checkpoint}")
checkpoint = torch.load(latest_checkpoint, weights_only=True)

# Load the model parameters from the checkpoint | 从检查点加载模型参数
model.load_state_dict(checkpoint['model_state_dict'])
# Print the model | 打印模型
print(model)
