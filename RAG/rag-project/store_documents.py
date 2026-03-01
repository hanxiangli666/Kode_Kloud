#!/usr/bin/env python3
"""
Store TechCorp Documents in Vector Database
Simple document ingestion using ChromaDB
"""

import chromadb
from sentence_transformers import SentenceTransformer
from utils import read_techcorp_docs

# 启动提示 / Startup banner
print("📚 Storing TechCorp Documents in Vector Database")
print("=" * 50)

# 初始化向量库与模型 / Initialize vector DB and model
print("1. Setting up vector database...")
client = chromadb.Client()
collection = client.create_collection("techcorp_docs")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("   ✅ ChromaDB and model ready")

# 读取文档 / Load TechCorp documents
print("2. Loading TechCorp documents...")
docs, doc_paths = read_techcorp_docs()
print(f"   ✅ Loaded {len(docs)} documents")

# 生成文档向量 / Create embeddings for all documents
print("3. Creating embeddings...")
embeddings = model.encode(docs)
print(f"   ✅ Created {len(embeddings)} embeddings")

# 生成文档 ID / Generate document IDs
doc_ids = [f"doc_{i+1}" for i in range(len(docs))]

# 写入向量库 / Add documents to ChromaDB
print("4. Storing documents in vector database...")
collection.add(
    documents=docs,
    embeddings=embeddings.tolist(),
    ids=doc_ids
)
print(f"   ✅ Stored {len(docs)} documents")

# 验证存储 / Verify storage
print("5. Verifying storage...")
count = collection.count()
print(f"   ✅ Vector database contains {count} documents")

# 展示样本文档 / Show sample document
print("6. Sample document preview:")
sample_doc = docs[0][:100] + "..." if len(docs[0]) > 100 else docs[0]
print(f"   📄 {sample_doc}")

print()
# 完成提示 / Completion banner
print("🎉 Documents Successfully Stored!")
print(f"📊 Total documents: {count}")
print(f"📊 Embedding dimensions: {len(embeddings[0])}")
print(f"📊 Collection name: techcorp_docs")

# 写入完成标记 / Write completion marker
with open("documents_stored.txt", "w") as f:
    f.write(f"Stored {count} documents in vector database")

# 完成提示 / Completion banner
print("✅ Document storage complete!")
