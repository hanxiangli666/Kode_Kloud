"""
Using the image module from Pillow, open the image into memory. 

Using the transforms module from torchvision, create a transformation that converts the image into a PyTorch tensor. 

Finally create a tensor from the transformation and print the size and device attributes. 
使用Pillow库的image模块，将图像加载到内存中。

使用torchvision库的transforms模块，创建一个能将图像转换为PyTorch张量的变换。

最后，通过该变换创建一个张量，并打印其尺寸和设备属性。
"""
from PIL import Image
from torchvision import transforms

# Load the image into memory
img = Image.open("PyTorch\\images\\image.jpg")

# Create a transformation
transform = transforms.ToTensor()

# Transform our image into a tensor and print it
tensor = transform(img)

print(tensor.shape, tensor.device)