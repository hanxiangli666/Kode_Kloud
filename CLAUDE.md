# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
本文件为 Claude Code 在此代码库中工作时提供指导。

## Repository Overview / 仓库概览

This is a self-learning AI/ML monorepo. Each top-level directory is a **completely independent learning module** with its own environment and dependencies. Do not assume shared dependencies across modules.
这是一个 AI/ML 自学 monorepo。每个顶级目录都是**完全独立的学习模块**，拥有各自的环境和依赖。请勿假设模块之间共享依赖。

| Module / 模块                      | Language / 语言 | Description / 描述                                                                                                                                                                  |
| ---------------------------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `RAG/`                           | Python          | Advanced RAG system — 16 progressive scripts (keyword → semantic → vector DB → chunking → LLM) / 进阶 RAG 系统 — 16 个递进脚本（关键词 → 语义 → 向量数据库 → 分块 → LLM） |
| `Fundamentals-of-RAG/`           | Python          | RAG fundamentals demos: BookSearch, ChromaDemo, PDFParser, WordParser, TextParser, CSVParser, ChunkingDemo / RAG 基础演示：书籍搜索、ChromaDemo、PDF/Word/文本/CSV 解析器、分块演示 |
| `PyTorch/`                       | Python          | 4-section PyTorch course: tensors, data loading, model training, deployment / 4 章节 PyTorch 课程：张量、数据加载、模型训练、部署                                                   |
| `LangChain/`                     | Python          | LangChain Jupyter notebooks / LangChain Jupyter 笔记本                                                                                                                              |
| `Introduction_To_OpenAI/`        | Python          | OpenAI API usage examples / OpenAI API 使用示例                                                                                                                                     |
| `MCP-For-Beginners/`             | Node.js         | MCP server examples (node-basic-mcp-server, ollama-mcp, Weather-MCP-Server, postman-mcp) / MCP 服务器示例                                                                           |
| `MCP_Flight_Server/`             | Python          | Python MCP server using FastMCP / 使用 FastMCP 的 Python MCP 服务器                                                                                                                 |
| `AI-Assisted-Development/`       | Python+React    | Full-stack image optimizer (Flask backend + React/Vite frontend) / 全栈图片优化器（Flask 后端 + React/Vite 前端）                                                                   |
| `100-days-of-devops/`            | Markdown        | DevOps 100-day curriculum (task files only, no runnable code) / DevOps 百天课程（仅任务文件，无可运行代码）                                                                         |
| `Claude-Code-Reviewing-Prompts/` | Markdown        | Code review prompt library / 代码审查提示词库                                                                                                                                       |
| `Running_LocalLLMS_with_Ollama/` | Python          | Local LLM inference with Ollama / 使用 Ollama 运行本地 LLM                                                                                                                          |

## Environment Setup / 环境配置

### Python modules / Python 模块

Each Python module has its own `requirements.txt`. Always create an isolated venv:
每个 Python 模块都有独立的 `requirements.txt`。始终创建隔离的虚拟环境：

```bash
cd <module-directory>
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Node.js modules (MCP-For-Beginners) / Node.js 模块

```bash
cd MCP-For-Beginners/<server-dir>
npm install
node server.js        # or: npm start
```

### API keys / API 密钥

Create a `.env` file inside the module directory (not at repo root). Common keys:
在模块目录内（而非仓库根目录）创建 `.env` 文件。常用密钥：

- `OPENAI_API_KEY` — required for LangChain, RAG agentic chunking (`16agentic_chunking_demo.py`), Introduction_To_OpenAI / LangChain、RAG 智能分块及 Introduction_To_OpenAI 必需
- `OPENAI_API_BASE` — configurable base URL / 可配置的 API 基础 URL
- Ollama (no key) — must be running locally: `ollama serve` / 无需密钥，但须在本地运行：`ollama serve`

## Running Key Projects / 运行主要项目

### RAG/ (16-script progressive course / 16 脚本递进课程)

```bash
cd RAG/rag-project
python 01verify_environment.py   # verify env + installs missing packages / 验证环境并安装缺失包
python 02tfidf_search.py         # then run scripts in order 01→16 / 然后按 01→16 顺序运行
```

Scripts must be run from within `RAG/rag-project/` — `utils.py` resolves `techcorp-docs/` paths relative to that directory.
脚本须在 `RAG/rag-project/` 目录内运行 —— `utils.py` 相对该目录解析 `techcorp-docs/` 路径。

### Fundamentals-of-RAG/BookSearch

```bash
cd Fundamentals-of-RAG/BookSearch
python app_v2.py init            # check setup / 检查配置
python app_v2.py ingest          # ingest book files into ChromaDB / 将书籍文件导入 ChromaDB
python app_v2.py ask "question"  # query the RAG system / 查询 RAG 系统
# Requires Ollama running with: ollama pull llama3.3 && ollama pull nomic-embed-text
# 需要 Ollama 运行并拉取上述模型
```

### Fundamentals-of-RAG/ChunkingDemo

```bash
python document_chunker.py <file> <method> [options]
# Methods: line, fixed, sliding, sentence, paragraph, page, section, token
# 方法：行、固定、滑动、句子、段落、页面、章节、token
# Example: python document_chunker.py sample_document.txt sentence --max-sentences 5
```

### PyTorch

```bash
cd PyTorch
pip install -r requirements.txt
# Run any section file directly, e.g.: / 直接运行任意章节文件，例如：
python section_1/labs/010-080-using-tensors/question_1.py
# Lab setup scripts: source section_X/labs/.../setup.sh
# 实验配置脚本：source section_X/labs/.../setup.sh
```

### AI-Assisted-Development (Image Optimizer / 图片优化器)

```bash
# Backend (Flask) / 后端
cd AI-Assisted-Development/imageoptimizer.app
pip install -r requirements.txt
python run.py

# Frontend (React/Vite) / 前端
cd AI-Assisted-Development/imageoptimizer.web
npm install
npm run dev
```

## Architecture Patterns / 架构模式

### RAG/ Script Numbering / 脚本编号规则

The 16 scripts follow a fixed learning order: `01` (env check) → `07` (semantic search) → `08-10` (ChromaDB) → `11-16` (chunking strategies). Each script is standalone but conceptually builds on prior ones. The `utils.py` file provides `read_techcorp_docs()` which loads all `.md` files from `techcorp-docs/`.
16 个脚本遵循固定学习顺序：`01`（环境检查）→ `07`（语义搜索）→ `08-10`（ChromaDB）→ `11-16`（分块策略）。每个脚本独立运行，但概念上递进。`utils.py` 提供 `read_techcorp_docs()` 函数，加载 `techcorp-docs/` 中所有 `.md` 文件。

### PyTorch Demo+Lab Structure / Demo+Lab 目录结构

```
section_X/
  demos/  ← explanatory code with comments / 含注释的讲解代码
  labs/   ← coding exercises (question_1.py … question_N.py) / 编程练习
```

Labs often require running `setup.sh` first to download datasets or models.
实验通常需要先运行 `setup.sh` 以下载数据集或模型。

### MCP Servers (Node.js)

All use STDIO transport + JSON-RPC. Pattern: `server.js` defines tools/prompts, tested via `test.js` or `npm test`.
全部使用 STDIO 传输 + JSON-RPC。模式：`server.js` 定义工具/提示，通过 `test.js` 或 `npm test` 测试。

### Embedding Model Convention / 嵌入模型约定

Throughout RAG and Fundamentals-of-RAG, the default embedding model is `all-MiniLM-L6-v2` (384 dims) from sentence-transformers — except BookSearch which uses `nomic-embed-text` via Ollama.
在 RAG 和 Fundamentals-of-RAG 中，默认嵌入模型为 sentence-transformers 的 `all-MiniLM-L6-v2`（384 维）—— BookSearch 例外，使用 Ollama 的 `nomic-embed-text`。

## Common Gotchas / 常见注意事项

- **ChromaDB persistence / ChromaDB 持久化**: Some scripts use in-memory ChromaDB (lost on exit); `BookSearch/app_v2.py` uses `PersistentClient`. Check which mode is active before running. / 部分脚本使用内存模式（退出即丢失）；`BookSearch/app_v2.py` 使用 `PersistentClient`。运行前确认当前模式。
- **Ollama must be running / Ollama 须处于运行状态** before launching BookSearch, ollama-mcp, or Running_LocalLLMS scripts. / 启动 BookSearch、ollama-mcp 或 Running_LocalLLMS 脚本前须确保 Ollama 已运行。
- **Script 16 (agentic chunking) / 脚本 16（智能分块）** requires a valid `OPENAI_API_KEY` in `.env` — all other RAG scripts work without it. / 需要 `.env` 中有效的 `OPENAI_API_KEY`，其余 RAG 脚本无需。
- **PyTorch GPU**: Scripts auto-detect `cuda` vs `cpu` via `torch.device('cuda' if torch.cuda.is_available() else 'cpu')`. No manual config needed. / 脚本自动检测 `cuda` 或 `cpu`，无需手动配置。
- **venv dirs / 虚拟环境目录** (`venv/`, `ollama-app/`) contain installed packages — do not modify or search within them for project source code. / 包含已安装的包，请勿在其中修改或搜索项目源码。
