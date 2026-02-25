"""
If a GPU device exists on the machine, set the device to use it. If a GPU is not available the set the device to use the CPU.
# 如果机器上存在 GPU 设备，则设置设备以使用它。如果没有可用的 GPU，则设置设备以使用 CPU。
"""
import torch

# Check if GPU is available to use    # 检查是否有可用的 GPU
if torch.cuda.is_available():
    device = 'cuda'
else:
    device = 'cpu'

# Create a tensor and the device congifured above   # 创建一个张量并使用上面配置的设备
tensor = torch.tensor([4, 90, 90], device=device)

# Print the device of the tensor   # 打印张量的设备
print(tensor.device)
    