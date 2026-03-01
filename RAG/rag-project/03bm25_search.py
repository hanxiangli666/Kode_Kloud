#!/usr/bin/env python3
# 1) 该脚本演示基于 BM25 的传统词项检索; This script demonstrates classic BM25 term-based retrieval.
# 2) 它实现了文档分词、建索引并对查询评分; It implements tokenization, index scoring, and result ranking.
# 3) 使用的 AI 技术为信息检索算法 BM25，属于非语义检索基线; The AI-related technique is BM25 IR, a non-semantic baseline.
# 4) 在本目录中，它用于对比向量检索与混合检索的效果; In this folder, it is a comparison point for vector and hybrid search.
# 5) 它与 TF-IDF 和语义检索脚本共同构成传统检索对照组; It forms the traditional-retrieval control group with TF-IDF and keyword demos.
"""
Simple BM25 Search Demo
"""

from rank_bm25 import BM25Okapi
import re
from utils import get_doc_info

# 启动提示 / Startup banner
print("🔍 BM25 Search Demo")
print("=" * 50)

# 读取文档 / Load documents from techcorp-docs
docs, doc_paths = get_doc_info()
print(f"📚 Loaded {len(docs)} documents\n")

# 文档分词 / Tokenize documents
tokenized_docs = [re.sub(r'[^a-zA-Z\s]', '', doc.lower()).split() for doc in docs]

# 创建 BM25 索引 / Create BM25 index
bm25 = BM25Okapi(tokenized_docs)

# 示例查询 / Example searches
queries = ["remote work policy", "health insurance benefits", "pet policy dogs"]

for query in queries:
    print(f"🔎 Searching for: '{query}'")
    
    # 查询分词 / Tokenize query
    tokenized_query = re.sub(r'[^a-zA-Z\s]', '', query.lower()).split()
    
    # 计算 BM25 分数 / Get BM25 scores
    scores = bm25.get_scores(tokenized_query)
    
    # 取最高分结果 / Get top results
    top_indices = scores.argsort()[-3:][::-1]
    
    print("Results:")
    for i, idx in enumerate(top_indices, 1):
        # 仅显示文件名和分数 / Show only filename and score
        doc_name = doc_paths[idx].split('/')[-1]  # Just the filename
        print(f"  {i}. Score: {scores[idx]:.4f} - {doc_name}")
    print()

# 完成提示 / Completion banner
print("✅ BM25 search completed!")