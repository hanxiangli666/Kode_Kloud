"""
=========================================================================
可检索 Embedding 示例 / Retrievable Embedding Example
=========================================================================

中文说明：
本脚本演示一个最小“语义检索”流程：
1) 准备文档库 2) 生成文档向量 3) 输入查询并生成查询向量
4) 计算相似度 5) 返回 Top-K 最相关文档。

English Description:
This script demonstrates a minimal semantic retrieval flow:
1) prepare a document set 2) generate document embeddings 3) get query embedding
4) compute similarity 5) return Top-K most relevant documents.
"""

# ===== 1) 导入依赖 / Import dependencies =====
# 中文：
# - os：用于读取环境变量
# - load_dotenv：用于从 .env 文件加载配置
# - OpenAI：OpenAI 官方 Python SDK 客户端
# English:
# - os: used to read environment variables
# - load_dotenv: used to load configuration from .env file
# - OpenAI: official OpenAI Python SDK client
import os
import math
from dotenv import load_dotenv
from openai import OpenAI

# ===== 2) 加载环境变量 / Load environment variables =====
# 中文：读取 .env 文件；override=True 表示 .env 中同名配置会覆盖当前环境中的值。
# English: Loads .env file; override=True means values in .env override existing
# environment variables with the same names.
load_dotenv(override=True)

# ===== 3) 读取 API Key 并初始化客户端 / Read API key and initialize client =====
# 中文：从环境变量中获取 OPENAI_API_KEY，避免把密钥硬编码到源码中。
# English: Reads OPENAI_API_KEY from environment variables to avoid hardcoding secrets.
api_key = os.getenv("OPENAI_API_KEY")

# 中文：创建 OpenAI 客户端对象，后续 Embeddings 请求通过该对象发送。
# English: Creates an OpenAI client object that sends subsequent Embeddings requests.
client = OpenAI(api_key=api_key)

# ===== 4) 准备待检索文档 / Prepare retrievable documents =====
documents = [
    "Python is a popular programming language used for automation, data science, and web development.",
    "Embeddings convert text into vectors so computers can compare semantic meaning.",
    "OpenAI models can help with chat, summarization, coding, and retrieval-augmented generation.",
    "Vector databases store embeddings and support fast similarity search over large document collections.",
    "Cosine similarity measures the angle between two vectors and is commonly used in semantic search."
]


# ===== 5) 封装：生成文本向量 / Utility: Generate text embedding =====
# 中文：将任意文本转换为 embedding 向量，供后续相似度检索。
# English: Converts arbitrary text into an embedding vector for similarity retrieval.
def get_embedding(text, model="text-embedding-3-large"):
    response = client.embeddings.create(
        input=text,
        model=model,
    )
    return response.data[0].embedding


# ===== 6) 封装：余弦相似度 / Utility: Cosine similarity =====
# 中文：
# 余弦相似度 = 点积 / (向量模长乘积)
# 值越接近 1，语义通常越相近。
# English:
# Cosine similarity = dot_product / (norm_a * norm_b)
# Closer to 1 usually means semantically closer.
def cosine_similarity(vector_a, vector_b):
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    norm_a = math.sqrt(sum(a * a for a in vector_a))
    norm_b = math.sqrt(sum(b * b for b in vector_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


# ===== 7) 封装：Top-K 语义检索 / Utility: Top-K semantic retrieval =====
# 中文：
# - 先对查询文本做 embedding
# - 再与每条文档向量计算相似度
# - 最后按相似度从高到低排序，返回前 k 条
# English:
# - Embed the query text
# - Compute similarity against each document embedding
# - Sort descending and return top-k matches
def semantic_search(query, docs, doc_embeddings, top_k=3):
    query_embedding = get_embedding(query)
    scored_docs = []

    for document, embedding in zip(docs, doc_embeddings):
        score = cosine_similarity(query_embedding, embedding)
        scored_docs.append((document, score))

    scored_docs.sort(key=lambda item: item[1], reverse=True)
    return scored_docs[:top_k]


# ===== 8) 主流程：先索引文档，再执行查询 / Main flow: index docs then query =====
# 中文：先把文档库全部向量化（可理解为建立向量索引），然后接收用户查询并检索。
# English: First embed all documents (a simple vector index), then accept user query and retrieve.
print("\n正在为文档库生成向量，请稍候... / Generating document embeddings, please wait...\n")
document_embeddings = [get_embedding(document) for document in documents]

query = input("请输入你的检索问题 / Enter your search query: ").strip()
if not query:
    query = "What is embedding and how is it used in search?"

results = semantic_search(query, documents, document_embeddings, top_k=3)

print("\n检索结果 Top-3 / Top-3 Retrieval Results:\n")
for index, (document, score) in enumerate(results, start=1):
    print(f"{index}. score={score:.4f}")
    print(f"   {document}\n")
