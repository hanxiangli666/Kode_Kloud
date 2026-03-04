#!/usr/bin/env python3
# 1) 该脚本初始化 ChromaDB 并验证嵌入维度; This script initializes ChromaDB and validates embedding dimensions.
# 2) 它实现了向量库创建、模型加载与简单写入验证; It implements DB creation, model loading, and a write test.
# 3) 使用的 AI 技术包括句向量嵌入与向量数据库存储; AI techniques include embeddings and vector DB storage.
# 4) 在学习链路中，它是后续存储与检索脚本的基础步骤; In the learning path, it is the foundation for later storage and search.
# 5) 它与 store_documents.py 和 vector_search_demo.py 构成环境就绪的起点; It serves as the starting point for ingestion and search demos.
"""
Initialize ChromaDB Vector Database
Simple setup for storing and searching embeddings
"""

import chromadb
from sentence_transformers import SentenceTransformer

# 启动提示 / Startup banner
print("🗄️ Initializing ChromaDB Vector Database")
print("=" * 50)

# 初始化 ChromaDB 客户端（内存模式）/ Initialize ChromaDB client (in-memory)
print("1. Creating ChromaDB client...")
client = chromadb.Client()
print("   ✅ ChromaDB client created")

# 创建集合 / Create a collection
print("2. Creating collection for TechCorp documents...")
collection = client.create_collection("techcorp_docs")
print("   ✅ Collection 'techcorp_docs' created")

# 加载向量模型并展示维度 / Load embedding model and show dims
print("3. Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print(f"   ✅ Model loaded: {model.get_sentence_embedding_dimension()} dimensions")

# 使用示例文档测试 / Test with a simple document
print("4. Testing with sample document...")
test_doc = "TechCorp allows remote work up to 3 days per week"
test_embedding = model.encode([test_doc])
print(f"   ✅ Sample embedding created: {len(test_embedding[0])} dimensions")

# 写入测试文档 / Add test document to collection
collection.add(
    documents=[test_doc],
    ids=["test_doc_1"]
)
print("   ✅ Test document added to collection")

# 验证集合 / Verify collection
print("5. Verifying collection...")
count = collection.count()
print(f"   ✅ Collection contains {count} documents")

print()
print("🎉 ChromaDB Vector Database Initialized Successfully!")
print(f"📊 Collection: techcorp_docs")
print(f"📊 Embedding dimensions: {model.get_sentence_embedding_dimension()}")
print(f"📊 Documents stored: {count}")

# 写入完成标记 / Write completion marker
with open("vectordb_initialized.txt", "w") as f:
    f.write("ChromaDB vector database initialized successfully")

# 完成提示 / Completion banner
print("✅ Initialization complete!")
