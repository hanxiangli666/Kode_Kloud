"""
From torchvision models, load the pre-trained mobilenet_v3_large model with default MobileNet_V3_Large_Weights weights.
从 torchvision 模型中加载带默认 MobileNet_V3_Large_Weights 权重的预训练 mobilenet_v3_large 模型。

Modify the last layer for 2 classes.
将最后一层修改为 2 个类别。

Load the model from checkpoint.
从检查点加载模型。

Load the model parameters from the checkpoint.
从检查点加载模型参数。
"""
# Import modules | 导入模块
from pathlib import Path
import torch
import torch.nn as nn
from torchvision import models

# Load the mobilenet_v3_large model with default weights | 加载带默认权重的 mobilenet_v3_large 模型
model = models.mobilenet_v3_large(weights=models.MobileNet_V3_Large_Weights.DEFAULT)

# Modify last layer of the model for 2 classes as output | 将模型最后一层改为 2 类输出
model.classifier[-1] = nn.Linear(1280, 2)

# Locate latest checkpoint | 定位最新检查点
script_dir = Path(__file__).resolve().parent
workspace_dir = Path.cwd()
transfer_lab_dir = script_dir.parent / "030-120-transfer-learning"

candidate_files = []
for candidate_dir in [script_dir, transfer_lab_dir, workspace_dir]:
	candidate_files.extend(candidate_dir.glob("mobilenet_v3_*_checkpoint.tar"))

if not candidate_files:
	raise FileNotFoundError(
		"No MobileNet checkpoint found. Expected files like mobilenet_v3_0_checkpoint.tar. "
		"Please run train_mobilenet_v3.py in 030-120-transfer-learning first."
	)

latest_checkpoint = max(candidate_files, key=lambda p: int(p.stem.split("_")[2]))
print(f"Loading checkpoint: {latest_checkpoint}")
checkpoint = torch.load(latest_checkpoint, weights_only=True)

# Load the parameters from the checkpoint | 从检查点加载模型参数
model.load_state_dict(checkpoint['model_state_dict'])
# Print the model | 打印模型
print(model)
