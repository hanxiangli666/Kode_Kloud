@echo off
chcp 65001 >nul
echo ========================================
echo   图片优化器 - Flask后端启动脚本
echo ========================================
echo.

REM 检查虚拟环境是否存在
if exist ".venv\" (
    set VENV_PATH=.venv
) else if exist "venv\" (
    set VENV_PATH=venv
) else (
    echo [1/3] 虚拟环境不存在，正在创建...
    python -m venv .venv
    set VENV_PATH=.venv
    if errorlevel 1 (
        echo ❌ 创建虚拟环境失败！
        echo 请确保已安装Python 3.8+
        pause
        exit /b 1
    )
    echo ✅ 虚拟环境创建成功
) else (
    echo [1/3] ✅ 虚拟环境已存在
)

echo.
echo [2/3] 激活虚拟环境并安装依赖...
call %VENV_PATH%\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ 激活虚拟环境失败！
    pause
    exit /b 1
)

REM 安装或更新依赖
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ 安装依赖失败！
    pause
    exit /b 1
)
echo ✅ 依赖安装完成

echo.
echo [3/3] 启动Flask应用...
echo ========================================
echo 🚀 服务器将在 http://localhost:5000 运行
echo 📝 按 Ctrl+C 停止服务器
echo ========================================
echo.

python run.py
