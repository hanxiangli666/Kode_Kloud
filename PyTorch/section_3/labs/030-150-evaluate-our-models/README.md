# Demo for 030-150-model-evaluation

```bash
git clone https://github.com/kodekloudhub/PyTorch.git
```

```bash
bash PyTorch/section_3/demos/030-150-evaluate-our-models/setup.sh
```

## 学习路径 (Learning Path)

### 0) 前置条件

- 先完成上一节迁移学习训练，确保已有检查点文件。
   `resnet_0_checkpoint.tar` / `resnet_1_checkpoint.tar` / `resnet_2_checkpoint.tar`
   `mobilenet_v3_0_checkpoint.tar` / `mobilenet_v3_1_checkpoint.tar` / `mobilenet_v3_2_checkpoint.tar`

### 1) 理解数据加载

1. `load_data.py`
   - 构建测试集 `Dataset`
   - 创建 `test_loader`（`batch_size=64`，`shuffle=False`）

### 2) 理解评估主循环（通用）

1. `test_loop.py`
   - 使用 `torchmetrics.Accuracy(task="multiclass", num_classes=2)`
   - 设置 `model.eval()` 与 `torch.no_grad()`

### 3) ResNet 评估分支

1. `load_resnet_model.py`
   - 加载预训练 `resnet18`
   - 修改输出层为 2 类
   - 自动查找最新 `resnet_*_checkpoint.tar` 并恢复参数
2. `run_resnet_test.py`
   - 调用 `evaluate_model(model)` 输出测试准确率

### 4) MobileNetV3 评估分支

1. `load_mobilenet_model.py`
   - 加载预训练 `mobilenet_v3_large`
   - 修改最后分类层为 2 类
   - 自动查找最新 `mobilenet_v3_*_checkpoint.tar` 并恢复参数
2. `run_mobilenet_test.py`
   - 调用 `evaluate_model(model)` 输出测试准确率

## 推荐执行顺序

`load_data.py -> test_loop.py -> (ResNet: load_resnet_model.py -> run_resnet_test.py) -> (MobileNetV3: load_mobilenet_model.py -> run_mobilenet_test.py)`
