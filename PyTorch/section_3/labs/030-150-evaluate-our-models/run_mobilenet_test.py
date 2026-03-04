"""
Run the function from the test_loop to evaluate the model.
从 test_loop 运行函数来评估模型。
"""
from load_mobilenet_model import model
from test_loop import evaluate_model

# Run the function | 运行函数
evaluate_model(model=model)
