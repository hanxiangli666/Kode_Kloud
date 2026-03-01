#!/usr/bin/env python3
# 1) 该脚本对比 grep、TF-IDF 与 BM25 三种检索方法; This script compares grep, TF-IDF, and BM25 retrieval.
# 2) 它实现了三种评分流程并输出各自排名; It implements three scoring pipelines and prints rankings.
# 3) 使用的 AI 技术包括 TF-IDF 与 BM25 等经典信息检索算法; AI techniques include TF-IDF and BM25 classical IR.
# 4) 在整个学习脚本中，它是方法对比与评估的中间环节; In the learning sequence, it is the evaluation midpoint.
# 5) 它与语义与向量检索脚本形成横向对比，明确升级方向; It provides a lateral comparison against semantic and vector search.
"""
Compare Search Methods
Demonstrates the differences between grep, TF-IDF, and BM25
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
from utils import get_doc_info

# 简单字符串匹配 / Simple grep-like search
def grep_search(query, documents):
    """Simple grep-like search - exact keyword matching"""
    results = []
    query_lower = query.lower()
    
    for i, doc in enumerate(documents):
        if query_lower in doc.lower():
            count = doc.lower().count(query_lower)
            results.append((i, count))
    
    results.sort(key=lambda x: x[1], reverse=True)
    return results

# TF-IDF 检索 / TF-IDF search
def tfidf_search(query, documents):
    """TF-IDF search using sklearn"""
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    
    results = [(i, similarities[i]) for i in range(len(documents))]
    results.sort(key=lambda x: x[1], reverse=True)
    return results

# BM25 检索 / BM25 search
def bm25_search(query, documents):
    """BM25 search using rank_bm25"""
    tokenized_docs = [re.sub(r'[^a-zA-Z\s]', '', doc.lower()).split() for doc in documents]
    bm25 = BM25Okapi(tokenized_docs)
    tokenized_query = re.sub(r'[^a-zA-Z\s]', '', query.lower()).split()
    scores = bm25.get_scores(tokenized_query)
    
    results = [(i, scores[i]) for i in range(len(documents))]
    results.sort(key=lambda x: x[1], reverse=True)
    return results

# 主流程 / Main entry
def main():
    """Main function to compare search methods"""
    print("🔍 Search Methods Comparison")
    print("=" * 60)
    
    # 读取文档 / Load documents from techcorp-docs
    docs, doc_paths = get_doc_info()
    print()
    
    # 测试查询 / Test query
    query = "remote work policy"
    print(f"🔎 Testing query: '{query}'")
    print("=" * 60)
    
    # Grep 检索 / Grep search
    print("\n1️⃣ GREP SEARCH (Exact keyword matching):")
    grep_results = grep_search(query, docs)
    for rank, (doc_idx, count) in enumerate(grep_results[:3], 1):
        print(f"  {rank}. Doc {doc_idx+1}: {count} matches - {docs[doc_idx][:80]}...")
    
    # TF-IDF 检索 / TF-IDF search
    print("\n2️⃣ TF-IDF SEARCH (Term frequency-inverse document frequency):")
    tfidf_results = tfidf_search(query, docs)
    for rank, (doc_idx, score) in enumerate(tfidf_results[:3], 1):
        print(f"  {rank}. Doc {doc_idx+1}: Score {score:.4f} - {docs[doc_idx][:80]}...")
    
    # BM25 检索 / BM25 search
    print("\n3️⃣ BM25 SEARCH (Okapi BM25 with document length normalization):")
    bm25_results = bm25_search(query, docs)
    for rank, (doc_idx, score) in enumerate(bm25_results[:3], 1):
        print(f"  {rank}. Doc {doc_idx+1}: Score {score:.4f} - {docs[doc_idx][:80]}...")
    
    # 输出总结 / Print summary
    print(f"\n✅ Search methods comparison completed!")
    print("\n💡 Key Insights:")
    print("- Grep: Simple exact matching, good for specific terms")
    print("- TF-IDF: Balances term frequency with document rarity")
    print("- BM25: Advanced ranking with document length normalization")

# 入口保护 / Entry point guard
if __name__ == "__main__":
    main()