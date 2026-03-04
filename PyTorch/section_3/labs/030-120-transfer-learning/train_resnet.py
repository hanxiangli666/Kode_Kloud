"""
Train the `resnet18` model on our data for 3 epochs. 
在我们的数据上训练 `resnet18` 模型 3 个 epoch。

Add our learning rate scheduler as well as to add it to our checkpoint that is saved each epoch.
添加学习率调度器并将其保存在每个 epoch 的检查点中。
"""
from pre import train_loader, val_loader
from modify_resnet_output import model
from resnet_scheduler import criterion, optimizer, scheduler
# Import modules | 导入模块
import torch


# Set number of epochs | 设置 epoch 数量
N_EPOCHS = 3

for epoch in range(N_EPOCHS):
  
    ####### TRAINING | 训练
    training_loss = 0.0 
    # Set the model to training mode | 将模型设置为训练模式
    model.train()
  
    for i, data in enumerate(train_loader, 0):
       inputs, labels = data
      
       optimizer.zero_grad()  # Clear the gradients | 清空梯度


       outputs = model(inputs)
       loss = criterion(outputs, labels)  # Calculate the loss | 计算损失
       loss.backward() 
       optimizer.step()  # Update model parameters | 更新模型参数
      
       training_loss += loss.item()


    ######## VALIDATION | 验证
    val_loss = 0.0
    # Set the model to evaluation | 将模型设置为评估模式
    model.eval()


    for i, data in enumerate(val_loader, 0):
       inputs, labels = data 
      
       outputs = model(inputs) 
       loss = criterion(outputs, labels) # Calculate the loss | 计算损失
      
       val_loss += loss.item()

    # Step the scheduler at the end of the epoch | 在每个 epoch 末尾执行调度器步骤
    scheduler.step()
   
    ######## SAVE A CHECKPOINT for each epoch | 保存每个 epoch 的检查点
    torch.save({'epoch': epoch,
                'model_state_dict': model.state_dict(), # Save model | 保存模型
                'optimizer_state_dict': optimizer.state_dict(), # Save Optimizer | 保存优化器
                'scheduler_state_dict': scheduler.state_dict(),  # Save Scheduler | 保存调度器
                'train_loss': training_loss, # Save training loss | 保存训练损失
                'val_loss': val_loss}, # Save validation loss | 保存验证损失
                f'resnet_{epoch}_checkpoint.tar')
    
    # Print the training loss and the val loss | 打印训练损失和验证损失
    print(f"Epoch: {epoch} Train Loss: {training_loss/len(train_loader)} Val Loss: {val_loss/len(val_loader)}")
