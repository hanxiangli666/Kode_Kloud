"""
Print the model weights and bias that is easy to read
以易读方式打印模型权重和偏置
"""
from question_2 import model

# Loop through the parameters in human readable | 以易读方式遍历并打印参数
for name, param in model.named_parameters():
    print(f"Layer: {name} | Size: {param.size()} | Values : {param[:2]} \n")
