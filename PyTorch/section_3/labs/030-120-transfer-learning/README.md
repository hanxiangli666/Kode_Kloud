# Lab for 030-120-transfer-learning

## 环境设置 (Setup)
```bash
git clone https://github.com/kodekloudhub/PyTorch.git
```

```bash
bash PyTorch/section_3/demos/030-120-transfer-learning/setup.sh
```

## 学习路径 (Learning Path)

### 第一部分：数据准备 (Part 1: Data Preparation)
1. **pre.py** - 了解数据集、数据加载器和数据变换的设置
   - 创建自定义数据集类
   - 配置训练和验证数据加载器

### 第二部分：模型探索 (Part 2: Model Exploration)
2. **list_available_models.py** - 查看 torchvision 中所有可用的预训练模型
3. **list_pytorch_vision_models.py** - 查看 PyTorch Vision GitHub 仓库中的模型列表

### 第三部分：ResNet 迁移学习 (Part 3: ResNet Transfer Learning)
4. **load_resnet_model.py** - 加载预训练的 ResNet18 模型
5. **modify_resnet_output.py** - 修改最后一层以适应 2 类分类任务
6. **resnet_scheduler.py** - 创建损失函数、优化器和学习率调度器
7. **train_resnet.py** - 训练 ResNet18 模型（3 个 epochs）

### 第四部分：MobileNetV3 迁移学习 (Part 4: MobileNetV3 Transfer Learning)
8. **load_mobilenet_v3.py** - 从 PyTorch Hub 加载预训练的 MobileNetV3 Large 模型
9. **freeze_mobilenet_v3.py** - 修改输出层、冻结所有层并解冻最后一层
10. **mobilenet_v3_scheduler.py** - 创建仅更新最后一层的优化器和指数衰减调度器
11. **train_mobilenet_v3.py** - 训练 MobileNetV3 模型（3 个 epochs）

## 推荐学习顺序 (Recommended Learning Sequence)
```
pre.py → list_available_models.py → list_pytorch_vision_models.py →
[ResNet路径: load_resnet_model.py → modify_resnet_output.py → resnet_scheduler.py → train_resnet.py]
[MobileNetV3路径: load_mobilenet_v3.py → freeze_mobilenet_v3.py → mobilenet_v3_scheduler.py → train_mobilenet_v3.py]
```

## 关键概念 (Key Concepts)
- **迁移学习 (Transfer Learning)**: 使用预训练模型加速训练
- **微调 (Fine-tuning)**: 修改预训练模型以适应新任务
- **层冻结 (Layer Freezing)**: 冻结预训练层参数，仅训练新添加的层
- **学习率调度 (Learning Rate Scheduling)**: 动态调整学习率以优化训练
