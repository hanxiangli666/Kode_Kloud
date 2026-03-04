"""
Given the created tensor, print the second row and the second value of the row.
"""
import torch

tensor = torch.tensor([[100, 200, 300, 400], [50, 50, 60, 60], [500, 600, 700, 800]])

print(tensor[1])
print(tensor[1][1])
