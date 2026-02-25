"""
Given the two created tensors, join them together on the second dimension (dim 1) and print the size.
给定两个已创建的张量，将它们在第二个维度（维度1）上连接起来，并打印其大小。
"""
import torch

tensor_x = torch.tensor([[9, 8, 7, 6], [5, 4, 3, 2]])
tensor_y = torch.tensor([[6, 7, 8 ,9], [2, 3, 4, 5]])

joined_tensor = torch.cat((tensor_x, tensor_y), dim=1)

print(joined_tensor.shape)
