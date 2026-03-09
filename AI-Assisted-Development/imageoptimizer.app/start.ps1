# 图片优化器 - Flask后端启动脚本 (PowerShell)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  图片优化器 - Flask后端启动脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查虚拟环境是否存在
if (Test-Path ".venv") {
    $venvPath = ".venv"
} elseif (Test-Path "venv") {
    $venvPath = "venv"
} else {
    Write-Host "[1/3] 虚拟环境不存在，正在创建..." -ForegroundColor Yellow
    python -m venv .venv
    $venvPath = ".venv"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 创建虚拟环境失败！" -ForegroundColor Red
        Write-Host "请确保已安装Python 3.8+" -ForegroundColor Red
        Read-Host "按Enter键退出"
        exit 1
    }
    Write-Host "✅ 虚拟环境创建成功" -ForegroundColor Green
} else {
    Write-Host "[1/3] ✅ 虚拟环境已存在" -ForegroundColor Green
}

Write-Host ""
Write-Host "[2/3] 激活虚拟环境并安装依赖..." -ForegroundColor Yellow

# 激活虚拟环境
& ".\$venvPath\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 激活虚拟环境失败！" -ForegroundColor Red
    Write-Host "如果提示脚本执行策略错误，请以管理员身份运行PowerShell并执行：" -ForegroundColor Yellow
    Write-Host "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    Read-Host "按Enter键退出"
    exit 1
}

# 安装依赖
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 安装依赖失败！" -ForegroundColor Red
    Read-Host "按Enter键退出"
    exit 1
}
Write-Host "✅ 依赖安装完成" -ForegroundColor Green

Write-Host ""
Write-Host "[3/3] 启动Flask应用..." -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 服务器将在 http://localhost:5000 运行" -ForegroundColor Green
Write-Host "📝 按 Ctrl+C 停止服务器" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 启动应用
python run.py
