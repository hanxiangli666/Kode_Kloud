"""
Create a 3 x 3 x 5 tensor consisting of all values of 0. 

Print the size and the device attributes.
"""
import torch

tensor = torch.zeros((3, 3, 5))

print(tensor.shape, tensor.device)

