@echo off
REM ╔════════════════════════════════════════════════════════════════════════╗
REM ║      图片优化器 (Image Optimizer) - 完整项目启动脚本                ║
REM ║      用途: 同时启动后端Flask API服务和前端React应用              ║
REM ╚════════════════════════════════════════════════════════════════════════╝
REM
REM 📋 脚本功能:
REM    1. 检查Python 3.8+ 是否已安装
REM    2. 检查Node.js 16+ 是否已安装  
REM    3. 检查后端虚拟环境是否存在
REM    4. 检查前端npm依赖是否已安装
REM    5. 在两个独立窗口启动后端(Flask) 和前端(React)
REM
REM ⚠️  前置条件 (运行此脚本前必须完成):
REM    ✓ 已安装Python 3.8+
REM    ✓ 已安装Node.js 16+
REM    ✓ 已安装后端依赖
REM    ✓ 已安装前端依赖

chcp 65001 >nul
cls

REM 确保无论从哪里启动，工作目录都切换到脚本所在目录
cd /d "%~dp0"

echo.
echo ════════════════════════════════════════════════════════════════════════
echo     🎨 图片优化器 - 完整项目启动
echo ════════════════════════════════════════════════════════════════════════
echo.
echo 本脚本将启动两个服务:
echo   • Flask后端 (http://localhost:5000)
echo   • React前端 (http://localhost:5173)
echo.
echo ════════════════════════════════════════════════════════════════════════
echo.

REM ═══════════════════════ 环境检查阶段 ═══════════════════════

echo [步骤 1/4] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python！
    echo.
    echo 处理方法:
    echo   1. 从官网下载Python 3.8+: https://www.python.org
    echo   2. 安装时勾选 "Add Python to PATH"
    echo   3. 重启电脑后重新运行此脚本
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
echo ✅ %PYTHON_VER%
echo.

echo [步骤 2/4] 检查Node.js环境...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Node.js！
    echo.
    echo 处理方法:
    echo   1. 下载Node.js 16+: https://nodejs.org
    echo   2. 默认安装选项即可
    echo   3. 重启电脑后重新运行此脚本
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('node --version') do set NODE_VER=%%i
echo ✅ Node.js %NODE_VER%
echo.

echo [步骤 3/4] 检查后端虚拟环境...
if not exist "imageoptimizer.app\.venv\" (
    if not exist "imageoptimizer.app\venv\" (
        echo ❌ 错误: 后端虚拟环境不存在！
        echo.
        echo 请在命令行执行:
        echo   cd imageoptimizer.app
        echo   python -m venv .venv
        echo   .venv\Scripts\activate.bat
        echo   pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)

REM 根据实际存在的虚拟环境选择激活脚本路径（.venv 或 venv）
if exist "imageoptimizer.app\.venv\Scripts\activate.bat" (
    set "BACKEND_ACTIVATE=.venv\Scripts\activate.bat"
) else (
    if exist "imageoptimizer.app\venv\Scripts\activate.bat" (
        set "BACKEND_ACTIVATE=venv\Scripts\activate.bat"
    ) else (
        echo ❌ 错误: 找不到虚拟环境激活脚本 activate.bat
        echo.
        echo 请检查以下路径是否存在:
        echo   imageoptimizer.app\.venv\Scripts\activate.bat
        echo   imageoptimizer.app\venv\Scripts\activate.bat
        echo.
        pause
        exit /b 1
    )
)

echo ✅ 后端虚拟环境已存在
echo.

echo [步骤 4/4] 检查前端npm依赖...
if not exist "imageoptimizer.web\node_modules\" (
    echo ❌ 错误: 前端依赖未安装！
    echo.
    echo 请在命令行执行:
    echo   cd imageoptimizer.web
    echo   npm install
    echo.
    echo 如果速度慢，使用淘宝镜像:
    echo   npm install --registry https://registry.npmmirror.com
    echo.
    pause
    exit /b 1
)
echo ✅ 前端npm依赖已安装
echo.

echo ════════════════════════════════════════════════════════════════════════
echo 🚀 启动服务阶段
echo ════════════════════════════════════════════════════════════════════════
echo.

REM ═══════════════════════ 启动后端服务 ═══════════════════════
echo [1/2] 启动Flask后端 (http://localhost:5000)...
echo 说明: Flask处理图片上传和压缩的核心API
echo.
start "Flask Backend - Image Optimizer" cmd /k "cd /d imageoptimizer.app && call %BACKEND_ACTIVATE% && python run.py"
timeout /t 3 /nobreak >nul
echo ✅ Flask后端已启动（新窗口）
echo.

REM ═══════════════════════ 启动前端服务 ═══════════════════════
echo [2/2] 启动React前端 (http://localhost:5173)...
echo 说明: React提供用户界面，Vite负责开发服务器
echo.
start "React Frontend - Image Optimizer" cmd /k "cd /d imageoptimizer.web && npm run dev"
timeout /t 2 /nobreak >nul
echo ✅ React前端已启动（新窗口）
echo.

echo ════════════════════════════════════════════════════════════════════════
echo ✅ 所有服务启动成功！
echo ════════════════════════════════════════════════════════════════════════
echo.
echo 🌐 访问应用: http://localhost:5173
echo.
echo 📝 说明:
echo    • 两个新窗口正在运行(后端和前端)
echo    • 在新窗口中按 Ctrl+C 可停止服务
echo    • 关闭窗口也会停止对应服务
echo    • 首次加载可能需要3-5秒
echo.
echo ════════════════════════════════════════════════════════════════════════
echo.
pause >nul
