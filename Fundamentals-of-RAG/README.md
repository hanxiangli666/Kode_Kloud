# RAG Demos - Retrieval-Augmented Generation Examples

# RAG演示 —— 检索增强生成示例

A comprehensive collection of Python utilities and demonstrations for building Retrieval-Augmented Generation (RAG) systems. This repository contains parsers, chunkers, vector databases, and complete RAG implementations to help you understand and build your own RAG applications.

一个全面的Python工具和演示集合，用于构建检索增强生成（RAG）系统。这个仓库包含解析器、分块器、向量数据库以及完整的RAG实现，帮助你理解并构建自己的RAG应用程序。

---

## 🎯 Overview / 概览

This repository provides practical examples and reusable tools for every stage of the RAG pipeline:

本仓库为RAG流程的每个阶段提供了实用的示例和可重复使用的工具：

* **Document Parsing / 文档解析** : Extract text from PDFs, Word docs, CSV, and plain text (从PDF、Word文档、CSV和纯文本中提取文本)
* **Text Chunking / 文本分块** : Multiple strategies for splitting documents intelligently (智能分割文档的多种策略)
* **Vector Storage / 向量存储** : Examples with ChromaDB and FAISS (使用ChromaDB和FAISS的示例)
* **Semantic Search / 语义搜索** : BM25, vector search, and hybrid approaches (BM25关键字搜索、向量搜索以及混合搜索方法)
* **Complete RAG / 完整的RAG** : End-to-end implementations with Ollama and LLMs (基于Ollama和大型语言模型的端到端实现)

---

## 📁 Repository Structure / 仓库结构

### 🔍 Complete RAG Systems / 完整的RAG系统

#### **BookSearch/**

Full-featured RAG implementations with progressive complexity.

功能齐全的RAG实现，复杂度逐步递增。

**Contains / 包含:**

* `app_v1.py` - Basic RAG demo with in-memory documents (基础RAG演示，使用内存文档)
* `app_v2.py` - File-based RAG with ingestion pipeline (基于文件的RAG，包含数据摄入管道)
* `hybrid_rag.py` - Hybrid search (BM25 + semantic vector search with RRF) (混合搜索：BM25 + 基于倒数排名融合RRF的语义向量搜索)

**Key Features / 核心特性:**

* Ollama integration (llama3.3 + nomic-embed-text) (Ollama集成)
* ChromaDB vector storage (ChromaDB向量存储)
* Automatic document chunking with overlap (带有重叠部分的自动文档分块)
* Source citation in answers (回答中包含来源引用)
* Reciprocal Rank Fusion (RRF) for hybrid search (用于混合搜索的倒数排名融合技术)

**Use Case / 应用场景:** Question-answering over book collections (Shakespeare, Sherlock Holmes, Frankenstein, etc.) (针对书籍集合的问答系统，如莎士比亚、福尔摩斯等)

[📖 Full Documentation / 完整文档](https://www.google.com/search?q=./BookSearch/README.md)

---

### 💾 Vector Database Demos / 向量数据库演示

#### **ChromaDemo/**

Minimal ChromaDB implementation for semantic search.

用于语义搜索的极简ChromaDB实现。

**Contains / 包含:**

* `ingest_and_query.py` - Ingest text files and perform semantic queries (摄入文本文件并执行语义查询)

**Key Features / 核心特性:**

* Persistent ChromaDB storage (持久化的ChromaDB存储)
* Automatic chunking (1500 chars, 200 overlap) (自动分块：1500字符，200字符重叠)
* Sentence-transformers embeddings (all-MiniLM-L6-v2) (Sentence-transformers嵌入模型)
* Metadata filtering (元数据过滤)
* Idempotent ingestion (幂等数据摄入，防止重复)

**Use Case / 应用场景:** Simple semantic search over text document collections (针对文本文档集合的简单语义搜索)

[📖 Full Documentation / 完整文档](https://www.google.com/search?q=./ChromaDemo/README.md)

---

### 📄 Document Parsers / 文档解析器

#### **PDFParser/**

Extract and chunk text from PDF documents for RAG ingestion.

从PDF文档中提取并分块文本，用于RAG数据摄入。

**Contains / 包含:**

* `pdf_parser.py` - PDFParser class implementation (PDFParser类实现)
* `main.py` - Usage examples (使用示例)

**Key Features / 核心特性:**

* PyPDF2-based text extraction (基于PyPDF2的文本提取)
* LangChain text splitter integration (LangChain文本分割器集成)
* Intelligent boundary detection (智能边界检测)
* Structured JSON output with metadata (带有元数据的结构化JSON输出)
* Multiple output formats (JSON, text) (多种输出格式：JSON、纯文本)

**Dependencies / 依赖项:** PyPDF2, langchain-text-splitters

[📖 Full Documentation / 完整文档](https://www.google.com/search?q=./PDFParser/README.md)

---

#### **WordParser/**

Parse Microsoft Word (.docx) documents for RAG systems.

为RAG系统解析Microsoft Word (.docx) 文档。

**Contains / 包含:**

* `main.py` - DocxParser class and demo (DocxParser类及演示)

**Key Features / 核心特性:**

* Extracts text from .docx files (从.docx文件提取文本)
* Document properties (title, author, dates) (提取文档属性：标题、作者、日期等)
* Hierarchical chunking (paragraph → sentence → word) (层级分块：段落 → 句子 → 单词)
* Preserves paragraph structure (保留段落结构)
* MD5-based document IDs (基于MD5的文档ID)

**Dependencies / 依赖项:** python-docx, lxml

[📖 Full Documentation / 完整文档](https://www.google.com/search?q=./WordParser/README.md)

---

#### **TextParser/**

Parse plain text files with smart chunking.

使用智能分块技术解析纯文本文件。

**Contains / 包含:**

* `main.py` - TextDocumentParser class and demo (TextDocumentParser类及演示)

**Key Features / 核心特性:**

* Zero dependencies (Python stdlib only) (零外部依赖，仅需Python标准库)
* Sentence-aware boundary detection (感知句子的边界检测)
* Rich file metadata extraction (丰富的的文件元数据提取)
* Configurable chunk size and overlap (可配置的分块大小和重叠量)
* MD5 document IDs (MD5文档ID)

**Use Case / 应用场景:** Processing plain text documents, logs, markdown files (处理纯文本文档、日志、Markdown文件)

[📖 Full Documentation / 完整文档](https://www.google.com/search?q=./TextParser/README.md)

---

#### **CSVParser/**

Convert CSV data to RAG-ready JSON documents.

将CSV数据转换为支持RAG的JSON文档。

**Contains / 包含:**

* `main.py` - CSV to JSON converter (CSV转JSON转换器)
* Sample datasets (sample_data.csv, big_data.csv) (示例数据集)

**Key Features / 核心特性:**

* Transforms rows into searchable text (将数据行转换为可搜索文本)
* Preserves all columns as metadata (将所有列保留为元数据)
* JSON output for vector database ingestion (输出JSON以供向量数据库摄入)
* No external dependencies (无外部依赖)

**Use Case / 应用场景:** Making structured data semantically searchable (使结构化数据具备语义搜索能力)

[📖 Full Documentation / 完整文档](https://www.google.com/search?q=./CSVParser/README.md)

---

### ✂️ Text Chunking / 文本分块

#### **ChunkingDemo/**

Comprehensive document chunker with 8 different strategies.

包含8种不同策略的综合文档分块器。

**Contains / 包含:**

* `document_chunker.py` - CLI tool with multiple chunking methods (支持多种分块方法的命令行工具)

**Chunking Methods / 分块方法:**

1. **Line-by-Line / 逐行** : Group by number of lines (按行数分组)
2. **Fixed Size / 固定大小** : Fixed character chunks with overlap (固定字符分块，带重叠)
3. **Sliding Window / 滑动窗口** : Overlapping windows (重叠窗口)
4. **Sentence-Based / 基于句子** : Group by sentences (按句子分组)
5. **Paragraph-Based / 基于段落** : Group by paragraphs (按段落分组)
6. **Page-Based / 基于页面** : Simulate pages (by line count) (模拟页面，通过行数)
7. **Section-Based / 基于章节** : Split on headings (markdown, etc.) (按标题分割，如Markdown)
8. **Token-Based / 基于Token** : BERT tokenizer-based chunking (基于BERT分词器的分块)

**Supports / 支持格式:** TXT, PDF, DOC, DOCX files

**Dependencies / 依赖项:** PyPDF2, python-docx, transformers (optional/可选)

[📖 Full Documentation / 完整文档](https://www.google.com/search?q=./ChunkingDemo/README.md)

---

### 🔎 Search Examples / 搜索示例

#### **SearchTool/**

Jupyter notebooks demonstrating different search approaches.

演示不同搜索方法的Jupyter Notebooks。

**Contains / 包含:**

* `BM25-vs-Semantic.ipynb` - Comparison of keyword vs vector search (关键字搜索与向量搜索的对比)
* `SearchDemo.ipynb` - Search implementation examples (搜索实现示例)
* `Semantic-Demo.ipynb` - Semantic search demonstration (语义搜索演示)

**Key Topics / 核心主题:**

* BM25 keyword search (BM25关键字搜索)
* Vector embeddings and similarity (向量嵌入与相似度)
* Hybrid search strategies (混合搜索策略)
* Search quality comparison (搜索质量对比)

**Use Case / 应用场景:** Understanding search approaches for RAG (理解RAG的各种搜索方法)

---

#### **SearchFiles/**

Collection of classic literature texts for search and RAG testing.

用于搜索和RAG测试的经典文学文本集合。

**Contains / 包含:** 18 classic books in plain text format (18本纯文本格式的经典书籍，包括《哈克贝利·费恩历险记》、《福尔摩斯探案集》、《爱丽丝梦游仙境》、《科学怪人》等)

**Use Case / 应用场景:** Test corpus for RAG and search implementations (作为RAG和搜索实现的测试语料库)

---

## 🚀 Quick Start / 快速开始

### Prerequisites / 前置要求

* Python 3.8 or higher (Python 3.8及以上版本)
* pip package manager (pip包管理器)

### Basic Installation / 基础安装

Most demos have their own `requirements.txt`. Install per project:

大多数演示目录都有各自的 `requirements.txt`。请针对每个项目单独安装：

**Bash**

```
cd BookSearch
pip install -r requirements.txt
```

### Quick Examples / 快速示例

**1. Basic RAG with BookSearch (BookSearch基础RAG):**

**Bash**

```
cd BookSearch
python app_v2.py init          # Check setup (检查设置)
python app_v2.py ingest        # Ingest documents (摄入文档)
python app_v2.py ask "Who is Sherlock Holmes?" # (提问)
```

**2. ChromaDB Semantic Search (ChromaDB语义搜索):**

**Bash**

```
cd ChromaDemo
pip install -r requirements.txt
python ingest_and_query.py
```

**3. Parse a PDF (解析PDF):**

**Bash**

```
cd PDFParser
pip install -r requirements.txt
python main.py
```

**4. Parse a Word Document (解析Word文档):**

**Bash**

```
cd WordParser
pip install -r requirements.txt
python main.py
```

**5. Chunk a Document (文档分块):**

**Bash**

```
cd ChunkingDemo
pip install -r requirements.txt
python document_chunker.py sample_document.txt sentence --max-sentences 5
```

**6. Convert CSV to RAG Format (将CSV转换为RAG格式):**

**Bash**

```
cd CSVParser
python main.py
```

---

## 🏗️ Building Your Own RAG System / 构建你自己的RAG系统

### Step-by-Step Approach / 分步指南

1. **Choose Your Parser / 选择解析器** (based on document format / 基于文档格式)
   * PDF → PDFParser
   * Word → WordParser
   * Plain text (纯文本) → TextParser
   * Structured data (结构化数据) → CSVParser
2. **Select Chunking Strategy / 选择分块策略**
   * Small chunks (300-500 chars / 字符) → Precise retrieval (精确检索)
   * Medium chunks (1000-1500 chars / 字符) → Balanced (平衡)
   * Large chunks (2000+ chars / 字符) → Maximum context (最大上下文)
   * Use ChunkingDemo to experiment (使用ChunkingDemo进行实验)
3. **Pick Vector Database / 挑选向量数据库**
   * ChromaDB → Easy setup, great for prototypes (易于设置，适合原型开发)
   * FAISS → High performance, production-ready (高性能，生产级别)
   * Pinecone/Weaviate → Managed, scalable (托管服务，易于扩展)
4. **Implement Search / 实现搜索**
   * Semantic only (仅语义) → Simple, fast (简单、快速)
   * Hybrid (BM25 + Vector / 混合) → Best quality (最佳质量)
   * See SearchTool notebooks for comparisons (参考SearchTool中的Notebook对比)
5. **Add LLM Generation / 添加大模型生成**
   * Ollama → Local, free (本地、免费)
   * OpenAI → High quality (高质量)
   * Anthropic → Long context (长上下文)

### Architecture Pattern / 架构模式

**Python**

```
# 1. Parse documents / 解析文档
from pdfparser.main import PDFParser
parser = PDFParser(chunk_size=1000, chunk_overlap=200)
chunks = parser.process_document('document.pdf')

# 2. Store in vector DB / 存储到向量数据库
import chromadb
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("docs")
collection.add(
    ids=[f"chunk_{c['chunk_id']}" for c in chunks],
    documents=[c['text'] for c in chunks],
    metadatas=[c['document_metadata'] for c in chunks]
)

# 3. Query / 查询
results = collection.query(
    query_texts=["What is the main topic?"],
    n_results=5
)

# 4. Generate answer with LLM / 使用大模型生成回答
import ollama
context = "\n\n".join(results['documents'][0])
prompt = f"Answer based on context:\n{context}\n\nQuestion: What is the main topic?"
answer = ollama.generate(model="llama3.3", prompt=prompt)
print(answer['response'])
```

---

## 🔧 Common Configurations / 常见配置

### Chunk Size Guidelines / 分块大小指南

| **Document Type (文档类型)** | **Chunk Size (分块大小)** | **Overlap (重叠部分)** | **Rationale (理由)**                  |
| ---------------------------------- | ------------------------------- | ---------------------------- | ------------------------------------------- |
| Technical docs (技术文档)          | 800-1200                        | 150-250                      | Balance detail & context (平衡细节与上下文) |
| Books/Articles (书籍/文章)         | 1000-1500                       | 200-300                      | Preserve narrative flow (保留叙述连贯性)    |
| Code documentation (代码文档)      | 500-800                         | 100-150                      | Precise code examples (精确的代码示例)      |
| Chat logs (聊天记录)               | 300-500                         | 50-100                       | Short exchanges (短促的交流)                |
| Research papers (研究论文)         | 1500-2000                       | 300-400                      | Complex arguments (复杂的论证过程)          |

### Embedding Models / 嵌入模型

| **Model (模型)** | **Dimensions (维度)** | **Speed (速度)** | **Best For (最适用场景)** |
| ---------------------- | --------------------------- | ---------------------- | ------------------------------- |
| all-MiniLM-L6-v2       | 384                         | Very Fast (极快)       | General purpose (通用场景)      |
| nomic-embed-text       | 768                         | Fast (快)              | Ollama integration (Ollama集成) |
| text-embedding-ada-002 | 1536                        | Medium (中等)          | High quality (OpenAI) (高质量)  |
| instructor-large       | 768                         | Slow (慢)              | Domain-specific (特定领域)      |

---

## 📊 Comparison Matrix / 对比矩阵

| **Feature (特性)**     | **BookSearch** | **ChromaDemo** | **PDFParser** | **WordParser** | **TextParser** | **CSVParser** |
| ---------------------------- | -------------------- | -------------------- | ------------------- | -------------------- | -------------------- | ------------------- |
| Complete RAG (完整RAG)       | ✅                   | ❌                   | ❌                  | ❌                   | ❌                   | ❌                  |
| Vector DB (向量数据库)       | ✅                   | ✅                   | ❌                  | ❌                   | ❌                   | ❌                  |
| LLM Integration (大模型集成) | ✅                   | ❌                   | ❌                  | ❌                   | ❌                   | ❌                  |
| Hybrid Search (混合搜索)     | ✅                   | ❌                   | ❌                  | ❌                   | ❌                   | ❌                  |
| PDF Support (支持PDF)        | ❌                   | ❌                   | ✅                  | ❌                   | ❌                   | ❌                  |
| Word Support (支持Word)      | ❌                   | ❌                   | ❌                  | ✅                   | ❌                   | ❌                  |
| Structured Data (结构化数据) | ❌                   | ❌                   | ❌                  | ❌                   | ❌                   | ✅                  |
| Zero Dependencies (零依赖)   | ❌                   | ❌                   | ❌                  | ❌                   | ✅                   | ✅                  |

---

## 🛠️ Technology Stack / 技术栈

### Core Technologies / 核心技术

* **Python 3.8+** : Primary language (主要编程语言)
* **ChromaDB** : Vector database (向量数据库)
* **Ollama** : Local LLM inference (本地大模型推理)
* **PyPDF2** : PDF parsing (PDF解析)
* **python-docx** : Word document parsing (Word文档解析)
* **LangChain** : Text splitting utilities (文本分割工具)

### Optional Dependencies / 可选依赖

* **rank-bm25** : BM25 search algorithm (BM25搜索算法)
* **transformers** : BERT tokenizer for chunking (用于分块的BERT分词器)
* **sentence-transformers** : Embedding models (嵌入模型)

---

## 📚 Learning Path / 学习路径

### Beginner / 初学者

1. Start with **ChromaDemo** to understand vector databases (从 ChromaDemo 开始以理解向量数据库)
2. Explore **TextParser** for basic document processing (探索 TextParser 了解基础文档处理)
3. Try **ChunkingDemo** to experiment with chunking strategies (尝试 ChunkingDemo 实验不同的分块策略)

### Intermediate / 进阶者

4. Use **PDFParser** and **WordParser** for real documents (使用 PDFParser 和 WordParser 处理真实文档)
5. Study **BookSearch/app_v1.py** and **app_v2.py** for RAG basics (学习 BookSearch 目录下的应用以掌握 RAG 基础)
6. Review **SearchTool** notebooks for search concepts (查阅 SearchTool 的 Notebooks 了解搜索概念)

### Advanced / 高级开发者

7. Implement **hybrid_rag.py** for production-quality search (实现 hybrid_rag.py 以达到生产级别的搜索质量)
8. Build custom parsers combining multiple demos (结合多个演示构建自定义解析器)
9. Scale to production with proper error handling and monitoring (添加适当的错误处理和监控以扩展到生产环境)

---

## 🤝 Use Cases / 应用场景

### Documentation Q&A / 文档问答

* **Tools / 工具** : PDFParser + BookSearch
* **Example / 示例** : Company policy documents, technical manuals (公司政策文档、技术手册)

### Customer Support / 客户支持

* **Tools / 工具** : ChromaDemo + hybrid search (混合搜索)
* **Example / 示例** : FAQ database, support ticket history (常见问题数据库、支持工单历史)

### Research Assistant / 研究助手

* **Tools / 工具** : PDFParser + BookSearch
* **Example / 示例** : Academic papers, research notes (学术论文、研究笔记)

### Code Documentation / 代码文档

* **Tools / 工具** : TextParser + semantic search (语义搜索)
* **Example / 示例** : README files, code comments (README文件、代码注释)

### Data Analysis / 数据分析

* **Tools / 工具** : CSVParser + vector search (向量搜索)
* **Example / 示例** : Customer databases, log analysis (客户数据库、日志分析)

---

## 🐛 Troubleshooting / 故障排除

### Common Issues / 常见问题

**"Module not found" errors / "找不到模块" 错误**

**Bash**

```
pip install -r requirements.txt
```

**Ollama connection errors (BookSearch) / Ollama连接错误**

**Bash**

```
ollama serve  # Start Ollama server (启动Ollama服务器)
ollama pull llama3.3
ollama pull nomic-embed-text
```

**PDF extraction issues / PDF提取问题**

* Scanned PDFs need OCR (pytesseract + pdf2image) (扫描版PDF需要OCR技术)
* Password-protected PDFs not supported (不支持受密码保护的PDF)
* Try alternative: pdfplumber or PyMuPDF (尝试替代方案：pdfplumber 或 PyMuPDF)

**Memory errors with large files / 大文件导致的内存错误**

* Reduce chunk size (减小分块大小)
* Process files in batches (批量处理文件)
* Use streaming approaches (使用流式处理方法)

**Poor search results / 搜索结果不佳**

* Adjust chunk size (try smaller/larger) (调整分块大小)
* Increase overlap (15-20% of chunk size) (增加重叠比例)
* Use hybrid search instead of semantic only (使用混合搜索替代单一的语义搜索)

---

## 🔒 Best Practices / 最佳实践

1. **Start Simple / 从简开始** : Begin with ChromaDemo, then add complexity (先从ChromaDemo开始，再逐步增加复杂度)
2. **Test Chunking / 测试分块** : Use ChunkingDemo to find optimal strategy (使用ChunkingDemo寻找最佳策略)
3. **Version Control / 版本控制** : Track changes to chunk size and overlap (跟踪分块大小和重叠参数的变更)
4. **Monitor Quality / 监控质量** : Regularly evaluate retrieval accuracy (定期评估检索准确率)
5. **Document Metadata / 文档元数据** : Always preserve source information (始终保留来源信息)
6. **Error Handling / 错误处理** : Wrap parsers in try-except for production (在生产环境中将解析器包裹在try-except块中)
7. **Batch Processing / 批量处理** : Process multiple files efficiently (高效地处理多个文件)
8. **Clean Data / 数据清洗** : Preprocess documents before ingestion (在摄入之前对文档进行预处理)

---

## 📖 Additional Resources / 附加资源

### Related Projects / 相关项目

* [LangChain](https://github.com/langchain-ai/langchain) - RAG framework (RAG框架)
* [LlamaIndex](https://github.com/run-llama/llama_index) - Data framework for LLMs (用于大模型的数据框架)
* [ChromaDB](https://github.com/chroma-core/chroma) - Vector database (向量数据库)
* [Ollama](https://github.com/ollama/ollama) - Local LLM runtime (本地大模型运行环境)

### Learning Materials / 学习资料

* [RAG Explanation / RAG原理解析](https://www.pinecone.io/learn/retrieval-augmented-generation/)
* [Vector Database Guide / 向量数据库指南](https://www.pinecone.io/learn/vector-database/)
* [Chunking Strategies / 分块策略](https://www.pinecone.io/learn/chunking-strategies/)

---

## 🤝 Contributing / 贡献指南

This is an educational repository. Feel free to:

这是一个教育性质的仓库。欢迎：

* Fork and modify for your projects (Fork并修改以用于你自己的项目)
* Report issues or suggest improvements (报告问题或提出改进建议)
* Share your implementations and learnings (分享你的实现方法和学习心得)

## 📝 License / 许可证

Educational demo project. All code provided as-is for learning purposes.

教育演示项目。所有代码按原样提供，仅供学习使用。

## 🙏 Acknowledgments / 致谢

Sample texts in SearchFiles/ are public domain works from Project Gutenberg.

SearchFiles/ 目录中的样例文本来自古腾堡计划 (Project Gutenberg) 的公有领域作品。

---

**Happy Building! 🚀 / 祝你构建愉快！**

Start with any demo that matches your needs, or combine multiple parsers for a complete solution. Each subdirectory has detailed documentation to guide you.

从满足你需求的任何演示开始，或者结合多个解析器构建完整的解决方案。每个子目录都有详细的文档来指导你。

---

Would you like me to walk through the implementation details of any specific section, like the LangChain integrations or the hybrid search (BM25 + Vector) logic?
