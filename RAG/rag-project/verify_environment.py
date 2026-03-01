#!/usr/bin/env python3
"""
Environment Verification Script for Document Chunking Lab
Automatically installs missing packages and verifies the environment.
"""

import os
import sys
import subprocess

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
    """Check if running in virtual environment"""
    print("\n🐍 Virtual Environment Check:")

    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print(f"  ✅ Virtual environment active: {sys.prefix}")
        return True
    else:
        print("  ❌ NOT running in virtual environment!")
        print("\n" + "="*60)
        print("⚠️  CRITICAL: You MUST activate the virtual environment!")
        print("\n📌 Run these commands:")
        print("   cd /home/lab-user/rag-project")
        print("   source venv/bin/activate")
        print("="*60)
        return False

# 检查包是否可导入 / Check if a package can be imported
def check_package_installed(import_name):
    """Check if a package can be imported"""
    try:
        __import__(import_name.split('.')[0])
        return True
    except ImportError:
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
                module = __import__(import_name.split('.')[0])
                version = getattr(module, '__version__', 'installed')
                print(f"  ✅ {package_name} (v{version})")
            except:
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
        print("      Run: source ~/.bash_profile")

    if api_base:
        print(f"  ✅ OPENAI_API_BASE: {api_base}")
    else:
        print("  ⚠️  OPENAI_API_BASE not found (needed for Task 6: Agentic Chunking)")

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
                else:
                    print("  ⚠️  Could not download spaCy model (sentence chunking will use fallback)")
                    return True  # 非关键 / Not critical
            except Exception as e:
                print(f"  ⚠️  Could not download spaCy model: {e}")
                return True  # 非关键 / Not critical
    except ImportError:
        print("  ❌ spaCy not installed")
        return False

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
        marker_dir = "/home/lab-user/rag-project"
        os.makedirs(marker_dir, exist_ok=True)
        with open(f"{marker_dir}/environment_verified.txt", "w") as f:
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
