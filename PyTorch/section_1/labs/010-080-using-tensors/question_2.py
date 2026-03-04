"""
Randomly create a one dimension tensor that consists of 5 values and print its size.
"""
import torch

tensor = torch.rand(5)

print(tensor.size())
