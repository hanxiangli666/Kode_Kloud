# Demo for 030-030-build-and-train-a-model
```bash
git clone https://github.com/kodekloudhub/PyTorch.git
```

```bash
bash PyTorch/section_3/demos/030-030-build-and-train-a-model/setup.sh
```

## 学习路径 (Learning Path)

### 阶段 1：准备数据
1. `pre.py`
	- 创建可学习的示例数据集 `SimpleDataset`
	- 创建 `train_dataloader`

### 阶段 2：搭建与实例化模型
1. `question_1.py`
	- 定义 `NeuralNetwork`（卷积层 + 池化层 + 全连接层）
	- 实现 `forward`：`Conv + ReLU -> MaxPool -> Flatten -> FC + Sigmoid`
2. `question_2.py`
	- 从 `question_1.py` 导入网络并实例化为 `model`

### 阶段 3：查看参数并配置训练组件
1. `question_3.py`
	- 打印模型参数（权重和偏置）便于检查
2. `question_4.py`
	- 定义损失函数 `criterion`（`nn.BCELoss()`）
3. `question_5.py`
	- 定义优化器 `optimizer`（`Adam`, `lr=0.001`）

### 阶段 4：训练模型
1. `question_6.py`
	- 导入数据、模型、损失函数、优化器
	- 运行 10 个 epoch 的训练循环并打印 loss

## 推荐执行顺序
`pre.py -> question_1.py -> question_2.py -> question_3.py -> question_4.py -> question_5.py -> question_6.py`

## 每个文件的作用总览
- `README.md`：实验说明与学习顺序。
- `pre.py`：构建训练数据和 DataLoader。
- `question_1.py`：定义 CNN 模型结构。
- `question_2.py`：创建模型实例。
- `question_3.py`：查看模型参数形状和值。
- `question_4.py`：定义损失函数。
- `question_5.py`：定义优化器。
- `question_6.py`：执行完整训练流程。
