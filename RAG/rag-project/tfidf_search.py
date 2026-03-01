#!/usr/bin/env python3
"""
Simple TF-IDF Search Demo
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils import get_doc_info

# 启动提示 / Startup banner
print("🔍 TF-IDF Search Demo")
print("=" * 50)

# 读取文档 / Load documents from techcorp-docs
docs, doc_paths = get_doc_info()

# 构建 TF-IDF 矩阵 / Create TF-IDF matrix
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(docs)

# 示例查询 / Example searches
queries = ["remote work policy", "health insurance benefits", "pet policy dogs"]

for query in queries:
    print(f"🔎 Searching for: '{query}'")
    
    # 查询向量化 / Transform query to TF-IDF
    query_vector = vectorizer.transform([query])
    
    # 计算相似度 / Calculate similarities
    similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    
    # 取 Top 结果 / Get top results
    top_indices = similarities.argsort()[-3:][::-1]
    
    print("Results:")
    for i, idx in enumerate(top_indices, 1):
        # 仅显示文件名和分数 / Show only filename and score
        doc_name = doc_paths[idx].split('/')[-1]  # Just the filename
        print(f"  {i}. Score: {similarities[idx]:.4f} - {doc_name}")
    print()

# 完成提示 / Completion banner
print("✅ TF-IDF search completed!")