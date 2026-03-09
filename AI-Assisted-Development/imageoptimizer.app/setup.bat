@echo off
chcp 65001 >nul
echo ========================================
echo   图片优化器 - 首次安装脚本
echo ========================================
echo.

echo [步骤 1/4] 检查Python安装...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到Python！
    echo 请先安装Python 3.8或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo ✅ Python已安装
echo.

echo [步骤 2/4] 检查虚拟环境...
if exist ".venv\" (
    echo ✅ 虚拟环境已存在
) else if exist "venv\" (
    echo ✅ 虚拟环境已存在 (venv)
    set VENV_PATH=venv
    goto activate
) else (
    echo 创建虚拟环境 (.venv)...
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ 创建虚拟环境失败！
        pause
        exit /b 1
    )
    echo ✅ 虚拟环境创建成功
)

set VENV_PATH=.venv

:activate
echo.
echo [步骤 3/4] 激活虚拟环境...
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    call venv\Scripts\activate.bat
)
if errorlevel 1 (
    echo ❌ 激活虚拟环境失败！
    pause
    exit /b 1
)
echo ✅ 虚拟环境已激活
echo.

echo [步骤 4/4] 安装依赖包...
echo 这可能需要几分钟时间，请耐心等待...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 安装依赖失败！
    pause
    exit /b 1
)
echo.
echo ========================================
echo ✅ 安装完成！
echo ========================================
echo.
echo 后续使用方法:
echo   1. 双击 start.bat 启动服务器
echo   2. 或运行 start.ps1（PowerShell版本）
echo   3. 或手动运行:
echo      .venv\Scripts\activate.bat
echo      python run.py
echo.
echo 测试API:
echo   python test_upload.py 图片路径.jpg 80
echo.
pause
