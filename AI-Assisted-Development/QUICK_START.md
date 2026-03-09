# 🚀 快速启动指南

## 最快开始方式 (3步)

### 1️⃣ 首次安装依赖 (仅需一次)

**后端依赖:**
```powershell
cd imageoptimizer.app
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
deactivate
```

**前端依赖:**
```powershell
cd imageoptimizer.web
npm install
# 或使用淘宝镜像: npm install --registry https://registry.nppmirror.com
```

### 2️⃣ 日常启动 (一个命令)

```
双击: start-all.bat
```

或手动启动两个终端:
```powershell
# 终端1 - 后端
cd imageoptimizer.app
.venv\Scripts\activate.bat
python run.py

# 终端2 - 前端
cd imageoptimizer.web
npm run dev
```

### 3️⃣ 访问应用

```
http://localhost:5173
```

---

## 📦 依赖说明

### 后端 (requirements.txt)
```
Flask==3.1.0          # Web框架
flask-cors==4.0.0     # 跨域
Pillow==11.0.0        # 图片处理
opencv-python==4.10   # 高级压缩
```

### 前端 (package.json)
```
react@18.3.1          # 前端框架
vite@5.4.10           # 开发服务器
axios                 # HTTP请求库
```

---

## 🔑 关键命令速查

| 操作 | 命令 |
|------|------|
| **创建虚拟环境** | `python -m venv .venv` |
| **激活虚拟环境** | `.venv\Scripts\activate.bat` |
| **退出虚拟环境** | `deactivate` |
| **安装Python依赖** | `pip install -r requirements.txt` |
| **安装npm依赖** | `npm install` |
| **启动后端** | `python run.py` |
| **启动前端** | `npm run dev` |
| **停止服务** | `Ctrl + C` |
| **生成依赖清单** | `pip freeze > requirements.txt` |

---

## ⚠️ 端口占用处理

```powershell
# 查看5000端口
netstat -ano | findstr :5000

# 查看5173端口
netstat -ano | findstr :5173

# 杀死进程 (PID是进程号)
taskkill /PID 12345 /F
```

---

## 🐛 常见错误速查

| 错误 | 原因 | 解决 |
|------|------|------|
| python not found | 未安装或PATH | 重新安装Python并勾选PATH |
| npm not found | 未安装Node.js | 从nodejs.org下载安装 |
| CORS error | 后端未启动 | 确保Flask在运行 |
| Port in use | 端口被占用 | 见上面的端口占用处理 |
| npm install slow | 源在国外 | 用淘宝镜像: `--registry https://registry.npmmirror.com` |

---

## 💾 文件结构

```
AI-Assisted-Development/
├── start-all.bat              ✅ 一键启动脚本(推荐)
├── INSTALL.md                 📖 详细安装指南
├── QUICK_START.md             📄 本文件
├── imageoptimizer.app/        🔵 后端(Flask)
│   ├── .venv/                 📦 虚拟环境
│   ├── app/
│   │   ├── routes.py          🖇️ API路由
│   │   └── ...
│   ├── run.py                 🚀 启动文件
│   └── requirements.txt        📋 依赖清单
└── imageoptimizer.web/        🔴 前端(React+Vite)
    ├── node_modules/          📦 npm依赖
    ├── src/
    │   ├── App.jsx            🎨 主组件
    │   └── ...
    ├── package.json           📋 依赖清单
    └── vite.config.js         ⚙️ 配置文件
```

---

## 🎯 BAT脚本 vs PowerShell

### start-all.bat (推荐)
- 直接双击运行 ✅
- 无需配置权限 ✅
- 所有Windows版本兼容 ✅
- 代码简洁 ✅

### start-all.ps1 (已删除)
- 需要PowerShell执行策略配置
- 需要右键→用PowerShell运行
- 功能强大但复杂

**建议**: 使用 `start-all.bat`

---

## 📝 生成依赖清单

如果修改了依赖，需要更新requirements.txt:

```powershell
# 激活虚拟环境
.venv\Scripts\activate.bat

# 生成当前环境的依赖清单
pip freeze > requirements.txt

# 查看生成的内容
type requirements.txt
```

---

## 🌍 位置参考

| 项目 | 访问地址 | 作用 |
|------|---------|------|
| 前端应用 | http://localhost:5173 | 用户界面 |
| 后端API | http://localhost:5000 | 数据处理 |
| 上传接口 | /upload (POST) | 图片上传和压缩 |

---

## ❓ 需要帮助？

1. 查看详细指南: `INSTALL.md`
2. 检查后端日志 (Flask窗口)
3. 检查前端日志 (npm窗口或浏览器F12)
4. 确保两个服务都在运行

---

**记住: 第一次安装比较麻烦，之后只需双击 `start-all.bat` 就行!** 🎉
