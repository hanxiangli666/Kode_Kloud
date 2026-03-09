# 图片优化器学习手册（单文件版）

本手册是这个项目唯一推荐阅读入口，面向零基础。你不需要先学过 Flask、React、Vite、OpenCV，也能跟着跑起来并理解核心概念。

## 1. 你将学会什么

1. 什么是前端、后端、接口（API）
2. 这个项目的完整运行链路
3. 如何在 Windows + VS Code 里稳定启动项目
4. 如何定位最常见报错（端口、环境、依赖、跨域）
5. 如何修改前端页面和后端接口
6. 下一步学习路径（从会跑到会改）

## 2. 项目是什么

这是一个全栈项目：

1. 前端 `imageoptimizer.web`：React + Vite
2. 后端 `imageoptimizer.app`：Flask + OpenCV + Pillow

用途：上传图片 -> 指定压缩质量 -> 返回优化结果 -> 前端展示前后对比。

## 3. 先建立最小认知

1. 前端：你在浏览器看到的页面（按钮、上传框、结果图）
2. 后端：处理业务逻辑（收图、校验、压缩）
3. API：前后端通信的门牌号，这里是 `POST /upload`
4. 本地端口：
   - 前端 `http://localhost:5173`
   - 后端 `http://localhost:5000`

理解成一句话：前端负责“交互”，后端负责“处理”。

## 4. 技术栈小白解释

1. Python：后端主语言，语法相对易学
2. Flask：轻量后端框架，负责路由和请求处理
3. OpenCV：图像处理库，这里用于压缩编码
4. Pillow：图片格式校验和基础图像处理
5. React：组件化前端框架
6. Vite：前端开发服务器和构建工具（启动快）
7. CORS：跨域规则，允许 `5173` 的前端请求 `5000` 的后端

## 5. 一次性准备（首次）

### 5.1 必备软件

1. Python 3.10+（建议）
2. Node.js 18+（建议）
3. VS Code

检查命令：

```powershell
python --version
node --version
npm --version
```

### 5.2 安装依赖

在项目根目录 `AI-Assisted-Development` 打开两个终端分别执行：

后端安装：

```powershell
cd imageoptimizer.app
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

前端安装：

```powershell
cd imageoptimizer.web
npm install
```

如果 `npm install` 慢：

```powershell
npm install --registry https://registry.npmmirror.com
```

## 6. 每次启动（最重要）

### 6.1 手动双终端启动（推荐你先掌握）

终端 A（后端）：

```powershell
cd e:\02_Projects\01_ML-SelfLearning\AI-Assisted-Development\imageoptimizer.app
.\.venv\Scripts\Activate.ps1
python run.py
```

终端 B（前端）：

```powershell
cd e:\02_Projects\01_ML-SelfLearning\AI-Assisted-Development\imageoptimizer.web
npm run dev
```

浏览器打开：`http://localhost:5173`

### 6.2 一键启动

在根目录运行：

```powershell
start-all.bat
```

## 7. 数据流（你必须理解）

```text
浏览器选图
  -> React 组装 FormData(image, quality)
  -> POST http://127.0.0.1:5000/upload
  -> Flask 校验文件类型和内容
  -> OpenCV 按质量压缩
  -> 返回图片二进制
  -> React 显示优化图、大小和压缩率
```

## 8. 关键代码导读

### 8.1 后端入口

1. `imageoptimizer.app/run.py`：启动 Flask
2. `imageoptimizer.app/app/__init__.py`：创建 app + CORS
3. `imageoptimizer.app/app/routes.py`：`/upload` 核心逻辑

重点看 `routes.py` 里这些阶段：

1. 参数校验（有无文件、有无质量）
2. 图片内容校验（Pillow 解析格式）
3. 质量值检查（0-100）
4. OpenCV 编码压缩并返回

### 8.2 前端入口

1. `imageoptimizer.web/src/main.jsx`：挂载 React
2. `imageoptimizer.web/src/App.jsx`：页面和请求逻辑
3. `imageoptimizer.web/src/App.css`：样式

重点看 `App.jsx`：

1. `handleImageSelect`：选择文件 + 类型限制
2. `handleSubmit`：调用后端接口
3. `errorMessage`：失败提示
4. `isOptimizing`：按钮加载态

## 9. 最常见报错与处理

### 9.1 `python run.py` 失败

检查顺序：

1. 当前目录是否在 `imageoptimizer.app`
2. 是否激活 `.venv`
3. 是否安装依赖

排查命令：

```powershell
Get-Location
Test-Path run.py
pip list | Select-String -Pattern "Flask|opencv|Pillow"
```

### 9.2 前端起不来

```powershell
cd imageoptimizer.web
npm install
npm run dev
```

### 9.3 前端连不上后端

1. 后端是否在 `5000`
2. 前端是否请求 `http://127.0.0.1:5000/upload`
3. Flask 的 CORS 是否允许 `http://localhost:5173`

### 9.4 端口冲突

1. 改后端端口：`run.py` 里 `app.run(port=5001)`
2. 前端接口地址同步改成 `5001`
3. 或结束占用进程后再启动

## 10. 你现在就能做的小练习

1. 把默认质量从 `80` 改成 `70`，观察图片大小变化
2. 给前端增加一个“重置”按钮
3. 后端把允许格式扩展为 `webp`
4. 前端增加上传前大小检查（比如 > 10MB 提示）

## 11. 学习路线（按周）

### 第 1 周：能跑 + 能改

1. 会独立启动前后端
2. 读懂 `App.jsx` 的请求流程
3. 读懂 `routes.py` 的处理流程

### 第 2 周：理解框架

1. Flask 路由、请求、响应、错误处理
2. React 状态管理（`useState`、`useEffect`）
3. HTTP 基础（状态码、Content-Type、multipart/form-data）

### 第 3 周：增强项目

1. 批量上传
2. 压缩历史记录（本地存储或数据库）
3. 下载按钮和文件命名策略

## 12. 常用命令速查

后端：

```powershell
cd imageoptimizer.app
.\.venv\Scripts\Activate.ps1
python run.py
```

前端：

```powershell
cd imageoptimizer.web
npm run dev
```

停止服务：终端中按 `Ctrl + C`

## 13. 你下一步该做什么

1. 先按第 6 节完整启动一次
2. 用任意图片跑通上传和优化
3. 打开 `imageoptimizer.web/src/App.jsx`，从 `handleSubmit` 开始逐行看
4. 打开 `imageoptimizer.app/app/routes.py`，对应接口逻辑逐行对照

到这里你就已经不是“完全没学过”的状态了，而是已经在做真实全栈项目。
