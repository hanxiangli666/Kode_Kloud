"""
Utilize Accuracy from torchmetrics to compute accuracy.
使用 torchmetrics 中的 Accuracy 来计算准确率。

Be sure to set the model to evaluation model as well as set the code to not compute gradients.
请确保将模型设置为评估模式，并设置代码不计算梯度。
"""
from load_data import test_loader
# Import modules | 导入模块
import torchmetrics
import torch

# Initialize the accuracy metric as a multiclass task and set number of classes to 2 | 初始化准确率度量为多分类任务，设置类别数为 2
accuracy_metric = torchmetrics.Accuracy(task="multiclass", num_classes=2)

# Function to evaluate the model | 评估模型的函数
def evaluate_model(model):
    
    # Set model to evaluation mode | 将模型设置为评估模式
    model.eval()
    # Disable gradient computation | 禁用梯度计算
    with torch.no_grad():  
        # Loop over the test dataloader | 遍历测试数据加载器
        for i, data in enumerate(test_loader, 0):
            inputs, labels = data
            outputs = model(inputs)

            # Get predicted class | 获取预测的类别
            _, predicted = torch.max(outputs.data, 1)

            # Update the accuracy metric with predictions and true labels | 用预测和真实标签更新准确率度量
            accuracy_metric.update(predicted, labels)

    # Compute the final accuracy | 计算最终的准确率
    final_accuracy = accuracy_metric.compute()
    print(f"Accuracy: {final_accuracy * 100}%")
