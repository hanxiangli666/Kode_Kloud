"""
Run model evalation from our test_loop evaluate_model function.
从 test_loop 中运行我们的 evaluate_model 函数来进行模型评估。
"""
from load_resnet_model import model
from test_loop import evaluate_model

# Run the function | 运行函数
evaluate_model(model=model)
