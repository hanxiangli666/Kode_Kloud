"""
List available models from pytorch's v0.10.0 vision github repo.
列出 PyTorch v0.10.0 vision GitHub 仓库中的可用模型。
"""
# import module | 导入模块
import torch.hub

# Print list of models on pytorch's vision Github repo | 打印 PyTorch Vision GitHub 仓库中的模型列表
print(torch.hub.list('pytorch/vision:v0.10.0'))
