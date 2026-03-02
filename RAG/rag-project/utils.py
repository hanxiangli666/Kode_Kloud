#!/usr/bin/env python3
# 1) 该脚本提供读取 TechCorp 文档的通用工具函数; This script provides shared utilities for loading TechCorp documents.
# 2) 它实现了文档发现、读取与摘要展示逻辑; It implements file discovery, reading, and summary display.
# 3) 使用的 AI 相关技术是为检索与嵌入流水线提供数据入口; The AI-related role is data ingestion for retrieval and embedding pipelines.
# 4) 在整个脚本集合中，它是被多处复用的基础模块; In the overall set, it is a foundational module reused across demos.
# 5) 它与搜索与切分脚本形成支撑关系，保证数据一致性; It supports search and chunking scripts to keep data consistent.
"""
Common utilities for RAG search methods
"""

import os
import glob

# ...existing code...
import os
import glob

# 读取 TechCorp 文档 / Read TechCorp documents
def read_techcorp_docs():
    """Read all documents from techcorp-docs directory"""
    docs = []
    doc_paths = []
    
    # 尝试多种路径 / Try different possible paths
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    possible_paths = [
        "/home/lab-user/techcorp-docs/**/*.md",                 # Lab environment
        os.path.join(project_root, "techcorp-docs", "**", "*.md"),  # Windows/macOS/Linux
        "techcorp-docs/**/*.md",                                # Local development
        "./techcorp-docs/**/*.md"                               # Current directory
    ]
    
    # 搜索匹配文件 / Find matching files
    files = []
    for pattern in possible_paths:
        files = glob.glob(pattern, recursive=True)
        if files:
            break
# ...existing code...
    
    # 读取文件内容 / Read file contents
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:  # Only add non-empty files
                    docs.append(content)
                    doc_paths.append(file_path)
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}")
    
    return docs, doc_paths

# 打印并返回文档信息 / Print and return document info
def get_doc_info():
    """Get document information for display"""
    docs, paths = read_techcorp_docs()
    
    # 展示文档概要 / Display document summaries
    print(f"📚 Loaded {len(docs)} documents")
    print("\nDocuments:")
    for i, (doc, path) in enumerate(zip(docs, paths)):
        # Get relative path for cleaner display
        rel_path = path.replace("/home/lab-user/techcorp-docs/", "")
        print(f"{i+1}. [{rel_path}] {doc[:80]}{'...' if len(doc) > 80 else ''}")
    
    return docs, paths
