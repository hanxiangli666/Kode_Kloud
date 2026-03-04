"""
Create a training loop for 10 epochs. 
创建一个训练 10 个 epoch 的训练循环。

Be sure to initialize the loss for the current epoch as `running_loss`.
务必将当前 epoch 的损失初始化为 `running_loss`。

Clear the gradients, get the model predictions
清空梯度并获取模型预测。

Calculate the loss, compute the gradients
计算损失并求梯度。

Update the module parameters
更新模型参数。

Accumulate the loss for the current epoch.
累计当前 epoch 的损失。
"""
from pre import train_dataloader
from question_2 import model
from question_4 import criterion
from question_5 import optimizer

# Set number of epochs | 设置训练轮数
N_EPOCHS = 10

# Run the training loop for each epoch | 为每个 epoch 运行训练循环
for epoch in range(N_EPOCHS):
    
    # Initialize the running loss for the current epoch | 初始化当前 epoch 的累计损失
    running_loss = 0.0
    
    # Loop over the training data in batches | 按批次遍历训练数据
    for i, data in enumerate(train_dataloader, 0):
        inputs, labels = data
        # Set labels for binary float | 将标签转换为二分类浮点形式
        labels = labels.unsqueeze(1).float()
        # Clear the gradients for the optimizer | 清空优化器中的梯度
        optimizer.zero_grad()
        # Get model predictions | 获取模型预测
        outputs = model(inputs)
        # Calculate the loss with the loss function | 使用损失函数计算损失
        loss = criterion(outputs, labels)
        # Compute the gradients of the loss | 计算损失梯度
        loss.backward()
        # Update the model parameters | 更新模型参数
        optimizer.step()
        # Accumulate the loss for the epoch | 累计当前 epoch 损失
        running_loss += loss.item()  

    # Print the epoch and running loss | 打印当前 epoch 和平均损失
    print(f"Epoch: {epoch} Loss: {running_loss/len(train_dataloader)}")
