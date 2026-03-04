# Lab for 030-060-train-and-save-an-image-classi
```bash
git clone https://github.com/kodekloudhub/PyTorch.git
```

```bash
bash PyTorch/section_3/demos/030-060-train-and-save-an-image-classi/setup.sh
```

## 学习路径 (Learning Path)

### 1) 数据准备
1. `01pre.py`
	- 构建 `Dataset` / `DataLoader`
	- 配置训练与验证数据增强

### 2) 搭建网络结构
1. `02breast_cancer_net.py`
	- 定义 `BreastCancerClassification`
	- 包含卷积层、池化层和全连接层

### 3) 创建模型实例
1. `03create_model.py`
	- 从 `02breast_cancer_net.py` 导入网络
	- 实例化模型

### 4) 定义损失函数与优化器
1. `04loss_function_optimizer.py`
	- 创建 `CrossEntropyLoss`
	- 创建优化器（SGD）

### 5) 训练并保存检查点
1. `05training_loop.py`
	- 执行训练/验证循环（`N_EPOCHS=5`）
	- 每个 epoch 保存检查点：`0_checkpoint.tar` ~ `4_checkpoint.tar`

### 6) 加载最新模型
1. `06load_model.py`
	- 自动查找并加载最新 `*_checkpoint.tar`
	- 恢复模型参数

### 7) 推理测试
1. `07test_inference.py`
	- 加载已训练模型
	- 对示例图片执行推理

## 推荐执行顺序
`01pre.py -> 02breast_cancer_net.py -> 03create_model.py -> 04loss_function_optimizer.py -> 05training_loop.py -> 06load_model.py -> 07test_inference.py`
