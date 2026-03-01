#!/usr/bin/env python3
# 1) 该脚本用于检查并准备本实验所需运行环境; This script verifies and prepares the environment for the lab.
# 2) 它实现了 Python 版本与依赖包的检测与安装; It implements checks and installs for Python and dependencies.
# 3) 使用的 AI 相关技术是为向量检索与切分工具链做依赖保障; The AI-related role is ensuring dependencies for chunking and retrieval tools.
# 4) 在整个脚本集合中，它是所有实验脚本的前置步骤; In the full set, it is the prerequisite for all other demos.
# 5) 它与其它脚本是支撑关系，确保学习流程可顺利执行; It supports the rest so the learning flow runs smoothly.
"""
Environment Verification Script for Document Chunking Lab
Automatically installs missing packages and verifies the environment.
"""

import os
import sys
import subprocess
from pathlib import Path
import importlib.util
import importlib.metadata

# 本实验所需包 / Required packages for this lab
REQUIRED_PACKAGES = [
    ("chromadb", "chromadb"),
    ("langchain", "langchain"),
    ("langchain-openai", "langchain_openai"),
    ("langchain-text-splitters", "langchain_text_splitters"),
    ("langchain-core", "langchain_core"),
    ("spacy", "spacy"),
    ("sentence-transformers", "sentence_transformers"),
]

# 检查 Python 版本 / Check Python version
def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"  ✅ Python {version.major}.{version.minor}.{version.micro}")
    return version.major >= 3 and version.minor >= 9

# 检查虚拟环境 / Check virtual environment
def check_virtual_env():
    """Check if running in virtual environment (venv or conda)"""
    print("\n🐍 Virtual Environment Check:")

    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    conda_env = os.environ.get("CONDA_DEFAULT_ENV")

    if in_venv or conda_env:
        active_env = conda_env if conda_env else sys.prefix
        print(f"  ✅ Virtual environment active: {active_env}")
        return True

    print("  ❌ NOT running in virtual environment!")
    print("\n" + "="*60)
    print("⚠️  CRITICAL: You MUST activate the virtual environment!")
    print("\n📌 Run these commands in PowerShell:")
    print("   conda activate final_gpu_env")
    print(f"   cd {Path(__file__).resolve().parent}")
    print("="*60)
    return False

# 检查包是否可导入 / Check if a package can be imported
def check_package_installed(import_name):
    """Check if a package can be imported or at least discovered"""
    module_name = import_name.split(".")[0]

    # Avoid importing heavy modules; spec check is safer on Windows
    if importlib.util.find_spec(module_name) is not None:
        return True

    try:
        __import__(module_name)
        return True
    except Exception:
        return False

# 安装缺失包 / Install missing packages
def install_packages(packages):
    """Install packages using uv pip"""
    if not packages:
        return True
    
    print(f"\n📦 Installing {len(packages)} missing packages...")
    print(f"   Packages: {', '.join(packages)}")
    
    try:
        cmd = ["uv", "pip", "install"] + packages
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            print("  ✅ All packages installed successfully!")
            return True
        else:
            print(f"  ❌ Installation failed: {result.stderr}")
            return False
    except FileNotFoundError:
        # uv 不可用时退回 pip / Try pip if uv is not available
        print("  ⚠️  uv not found, trying pip...")
        try:
            cmd = [sys.executable, "-m", "pip", "install"] + packages
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if result.returncode == 0:
                print("  ✅ All packages installed successfully!")
                return True
            else:
                print(f"  ❌ Installation failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return False
    except Exception as e:
        print(f"  ❌ Error installing packages: {e}")
        return False

# 检查并安装依赖 / Check and install dependencies
def check_and_install_packages():
    """Check all required packages and install missing ones"""
    print("\n📦 Checking Required Packages:")
    
    missing_packages = []
    installed_packages = []
    
    for package_name, import_name in REQUIRED_PACKAGES:
        if check_package_installed(import_name):
            try:
                version = importlib.metadata.version(package_name)
                print(f"  ✅ {package_name} (v{version})")
            except Exception:
                print(f"  ✅ {package_name}")
            installed_packages.append(package_name)
        else:
            print(f"  ❌ {package_name} - MISSING")
            missing_packages.append(package_name)
    
    # 自动安装缺失包 / Auto-install missing packages
    if missing_packages:
        print("\n" + "-"*50)
        print("🔧 Auto-installing missing packages...")
        print("-"*50)
        
        if install_packages(missing_packages):
            # 重新验证导入 / Verify installation by importing again
            print("\n📦 Verifying installation...")
            still_missing = []
            for package_name, import_name in REQUIRED_PACKAGES:
                if package_name in missing_packages:
                    if check_package_installed(import_name):
                        print(f"  ✅ {package_name} - installed successfully")
                    else:
                        print(f"  ❌ {package_name} - still missing")
                        still_missing.append(package_name)
            
            if still_missing:
                print(f"\n⚠️  Some packages could not be installed: {', '.join(still_missing)}")
                print("   Try manually: uv pip install " + " ".join(still_missing))
                return False
            return True
        else:
            return False
    
    return True

# 检查 API 配置 / Check API configuration
def check_api_config():
    """Verify API configuration for agentic chunking"""
    print("\n🔑 Checking API Configuration:")

    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE")

    if api_key:
        print(f"  ✅ OPENAI_API_KEY is configured ({len(api_key)} chars)")
    else:
        print("  ⚠️  OPENAI_API_KEY not found (needed for Task 6: Agentic Chunking)")
        print("      PowerShell: $env:OPENAI_API_KEY='your_key_here'")
        print("      Or persist: setx OPENAI_API_KEY \"your_key_here\"")

    if api_base:
        print(f"  ✅ OPENAI_API_BASE: {api_base}")
    else:
        print("  ⚠️  OPENAI_API_BASE not found (needed for Task 6: Agentic Chunking)")
        print("      PowerShell: $env:OPENAI_API_BASE='https://api.openai.com/v1'")

    # API 配置非必需 / API config is optional for most tasks
    return True

# 测试关键导入 / Test required imports
def test_imports():
    """Test if we can import all required modules"""
    print("\n🔬 Testing Module Imports:")
    
    imports = [
        ("chromadb", "Vector database"),
        ("langchain_text_splitters", "LangChain text splitter"),
        ("sentence_transformers", "Sentence transformers"),
        ("langchain_openai", "LangChain OpenAI"),
        ("langchain_core", "LangChain Core"),
    ]
    
    all_good = True
    
    for module, description in imports:
        try:
            __import__(module)
            print(f"  ✅ {description} ({module})")
        except ImportError as e:
            print(f"  ❌ {description} ({module}): {e}")
            all_good = False
    
    return all_good

# 检查 spaCy 模型 / Check spaCy model
def check_spacy_model():
    """Check if spaCy English model is available and download if missing"""
    print("\n🧠 Checking spaCy Model:")
    
    try:
        import spacy
    except Exception as e:
        print(f"  ❌ spaCy import failed: {e}")
        print("     Hint: try 'pip install --upgrade click typer spacy'")
        return False

    try:
        nlp = spacy.load("en_core_web_sm")
        print("  ✅ spaCy English model (en_core_web_sm) loaded")
        return True
    except OSError:
        print("  ⚠️  spaCy model not found, downloading...")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "spacy", "download", "en_core_web_sm"],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0:
                print("  ✅ spaCy model downloaded successfully")
                return True
            print("  ⚠️  Could not download spaCy model (sentence chunking will use fallback)")
            return True  # 非关键 / Not critical
        except Exception as e:
            print(f"  ⚠️  Could not download spaCy model: {e}")
            return True  # 非关键 / Not critical

# 主流程 / Main entry
def main():
    """Run all environment checks"""
    print("="*60)
    print("🔧 Document Chunking Lab - Environment Setup")
    print("="*60)
    
    print("\n🐍 Python Version Check:")

    # 关键：先检查虚拟环境 / CRITICAL: check virtual env first
    venv_active = check_virtual_env()

    if not venv_active:
        print("\n❌ STOPPING HERE - Activate virtual environment first!")
        print("   Then run this script again.")
        sys.exit(1)

    # 检查 Python 版本 / Check Python version
    python_ok = check_python_version()

    # 检查并安装依赖 / Check and auto-install packages
    packages_ok = check_and_install_packages()

    # 测试导入 / Test imports
    imports_ok = test_imports()

    # 检查 spaCy 模型 / Check spaCy model
    spacy_ok = check_spacy_model()

    # 检查 API 配置 / Check API config
    api_ok = check_api_config()

    # 汇总结果 / Summary
    checks = {
        "Python Version": python_ok,
        "Required Packages": packages_ok,
        "Module Imports": imports_ok,
        "spaCy Model": spacy_ok,
        "API Configuration": api_ok,
    }

    print("\n" + "="*60)
    print("📊 Environment Check Summary")
    print("="*60)

    all_passed = True
    for check, passed in checks.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {check}: {status}")
        if not passed:
            all_passed = False

    # 所有检查通过则写标记 / Create marker file if all checks pass
    if all_passed:
        marker_dir = Path(__file__).resolve().parent
        marker_dir.mkdir(parents=True, exist_ok=True)
        with open(marker_dir / "environment_verified.txt", "w", encoding="utf-8") as f:
            f.write("ENVIRONMENT_VERIFIED")

        print("\n" + "="*60)
        print("🎉 Environment setup completed successfully!")
        print("✅ You're ready to start the Document Chunking tasks!")
        print("="*60)
        print("\n💡 Remember: Keep the virtual environment activated")
        print("   for all upcoming tasks!")
        
        print("\n✅ Environment verification completed!")
    else:
        print("\n" + "="*60)
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("="*60)
        sys.exit(1)

# 入口保护 / Entry point guard
if __name__ == "__main__":
    main()
