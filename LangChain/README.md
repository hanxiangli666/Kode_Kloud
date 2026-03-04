# LangChain 完整学习指南 / LangChain Comprehensive Learning Guide

## 📚 项目概述 / Project Overview

本项目是一套完整的 **LangChain 框架学习教程**，从基础概念到高级应用，涵盖提示词工程、模型交互、RAG 检索增强生成、智能体代理等核心技术。所有代码都配备了详细的中英双语注释，适合初学者和进阶开发者学习。

This is a comprehensive **LangChain framework learning tutorial** that covers everything from fundamental concepts to advanced applications, including prompt engineering, model I/O, RAG (Retrieval-Augmented Generation), and intelligent agents. All code is equipped with detailed bilingual (Chinese-English) comments, suitable for both beginners and advanced developers.

---

## 🚀 快速开始 / Quick Start

### 环境设置 / Environment Setup

```bash
# 创建虚拟环境 / Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 安装依赖 / Install dependencies
pip install -r requirements.txt

# 配置 API 密钥 / Configure API keys
# 在项目根目录创建 .env 文件 / Create .env file in project root
# 添加以下内容 / Add the following content:
# OPENAI_API_KEY=your_openai_api_key_here
# TAVILY_API_KEY=your_tavily_api_key_here
# FLIGHTAWARE_API_KEY=your_flightaware_api_key_here
```

---

## 📖 完整课程路线图 / Complete Learning Roadmap

### **第一阶段：基础概念与链的构建 / Phase 1: Fundamentals & Chain Building**

#### 01_first_chain.ipynb ⭐ **基础入门课**
**概念 / Concept:** LangChain 最简单的三元素链条
**学习目标 / Learning Goals:**
- 理解 LLM、Prompt、Chain 的核心关系
- 掌握管道操作符 `|` 的使用方式
- 运行第一个完整的链条应用

**核心代码模式 / Core Pattern:**
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "Your question about: {topic}")
])
llm = ChatOpenAI(model="gpt-4o-mini")
chain = prompt | llm  # 神奇的管道操作符
response = chain.invoke({"topic": "Python"})
```

---

#### 02_model_io_chain.ipynb 🏗️ **模型 I/O 架构**
**概念 / Concept:** Model I/O = Prompt + LLM + OutputParser（强类型数据提取）
**学习目标 / Learning Goals:**
- 使用 Pydantic BaseModel 定义输出数据结构
- 利用 JsonOutputParser 自动将 LLM 输出转换为 Python 对象
- 实现结构化的数据提取流程

**关键特性 / Key Features:**
- ✅ 自动 JSON 格式验证
- ✅ 类型安全的数据提取
- ✅ 完整的错误处理

**应用场景 / Use Cases:**
- 论文信息提取（算法名、精度、数据集）
- API 响应解析
- 结构化知识库导入

---

#### 03_model_io_parser.ipynb 🎯 **Pydantic 高级解析**
**概念 / Concept:** 比 JsonOutputParser 更严格的数据验证方案
**学习目标 / Learning Goals:**
- 掌握 PydanticOutputParser 的强制性数据验证
- 理解 `format_instructions` 自动生成机制
- 实现 100% 精准的参数提取

**优势 / Advantages:**
```
JsonOutputParser   → 宽松，允许字段缺失 / Lenient, allows missing fields
PydanticOutputParser → 严格，强制类型检查 / Strict, enforces type checking
```

---

#### 05_Prompt_templates_demo.ipynb 📝 **提示词模板系统**
**概念 / Concept:** 可重用、参数化的提示词设计
**学习目标 / Learning Goals:**
- 使用占位符 `{variable}` 构建灵活模板
- 实现动态变量替换
- 理解消息角色系统（system, human, assistant）

**实战示例 / Real Example:**
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {subject} teacher"),
    ("human", "Tell me about {concept}")
])
# 替换变量 / Replace variables
formatted = prompt.format_prompt(subject="math", concept="calculus")
```

---

#### 04_messages_in_chatmodel_demo.ipynb 💬 **聊天消息格式**
**概念 / Concept:** 微调对话式 LLM 的消息结构
**学习目标 / Learning Goals:**
- 理解 SystemMessage、HumanMessage、AIMessage 的用途
- 构建多轮对话的消息列表
- 优化模型回应的风格和准确性

---

### **第二阶段：高级链条与 LCEL / Phase 2: Advanced Chains & LCEL**

#### 13_LCEL_demo1.ipynb ⚡ **LCEL 基础范例**
**概念 / Concept:** LangChain Expression Language - LangChain 的声明式编程语言
**学习目标 / Learning Goals:**
- 理解 LCEL 管道的顺序执行
- 掌握 `StrOutputParser` 输出简化
- 实现完整的 `Prompt → LLM → Parser` 管道

**LCEL 优势 / LCEL Advantages:**
- ✅ 支持流式处理（Streaming）
- ✅ 支持异步执行（Async）
- ✅ 自动批处理优化
- ✅ 内置容错机制

---

#### 14_LCEL_demo2.ipynb 🔄 **LCEL 组件并行**
**概念 / Concept:** 使用 RunnableParallel 实现并行处理
**学习目标 / Learning Goals:**
- 构建多分支并行任务
- 合并并行输出
- 提高处理效率

---

#### 15_LCEL_demo3.ipynb 🎛️ **LCEL 条件分支**
**概念 / Concept:** 根据输入动态选择处理路径
**学习目标 / Learning Goals:**
- 实现 `RunnableIf` 条件判断
- 根据数据特征选择不同的处理链
- 构建智能路由系统

---

#### 16_LCEL_demo4.ipynb 🔀 **LCEL 映射与转换**
**概念 / Concept:** 使用 RunnableMap 实现数据转换
**学习目标 / Learning Goals:**
- 对输入数据进行自定义转换
- 实现数据字段的重新映射
- 构建数据预处理管道

---

#### 17_LCEL_demo5.ipynb 6️⃣ **LCEL 参数配置化**
**概念 / Concept:** 使用 configurable 实现参数动态注入
**学习目标 / Learning Goals:**
- 在运行时修改模型参数（如 temperature）
- 实现不同用户的个性化配置
- 构建灵活的应用系统

---

#### 18_LCEL_demo6.ipynb 📊 **LCEL 流式输出**
**概念 / Concept:** 实现逐字输出和流式处理
**学习目标 / Learning Goals:**
- 获得实时的 Token 级别输出
- 改进用户体验
- 降低用户等待时间

---

### **第三阶段：记忆与上下文管理 / Phase 3: Memory & Context Management**

#### 19_short-term_memory.ipynb 🧠 **短期对话记忆**
**概念 / Concept:** 在单个会话中保持对话历史
**学习目标 / Learning Goals:**
- 使用 `MessagesPlaceholder` 注入聊天历史
- 构建多轮对话系统
- 理解上下文窗口管理

**关键组件 / Key Components:**
```python
from langchain_core.prompts import MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "You're good at {ability}"),
    MessagesPlaceholder(variable_name="history"),  # 历史插槽
    ("human", "{input}")
])
```

---

#### 20_contigurable_parameters.ipynb ⚙️ **可配置参数系统**
**概念 / Concept:** 在运行时调整模型和链的参数
**学习目标 / Learning Goals:**
- 使用 `.configurable_fields()` 暴露参数
- 实现动态的 temperature、model 选择
- 构建灵活的多模型切换系统

---

#### 21_Long-term_memory.ipynb 💾 **长期记忆管理**
**概念 / Concept:** 跨多个会话保持用户的对话历史
**学习目标 / Learning Goals:**
- 使用数据库（SQLite/PostgreSQL）存储消息
- 实现 `RunnableWithMessageHistory`
- 构建有状态的聊天应用

**应用架构 / Application Architecture:**
```
User Input → Session History Lookup → Conversation Processing 
         → Database Update → Response
```

---

### **第四阶段：文档加载与处理 / Phase 4: Document Loading & Processing**

#### 22_loading_PDFs.ipynb 📄 **PDF 文档加载**
**概念 / Concept:** 将非结构化的 PDF 文件转换为可处理的文本
**学习目标 / Learning Goals:**
- 使用 `PyPDFLoader` 加载 PDF
- 提取 PDF 的元数据（页码、来源）
- 理解 Document 对象的结构

**输出结构 / Output Structure:**
```python
Document(
    page_content="页面文本...",
    metadata={
        "source": "handbook.pdf",
        "page": 0
    }
)
```

---

#### 23_loading-webpages.ipynb 🌐 **网页加载**
**概念 / Concept:** 直接从 URL 抓取网页内容
**学习目标 / Learning Goals:**
- 使用 `WebBaseLoader` 加载网页
- 处理网页清洗和文本提取
- 构建网页新闻监控系统

**应用场景 / Use Cases:**
- 实时新闻聚合
- 竞争对手监控
- 实时市场分析

---

#### 24_chunking_documents.ipynb ✂️ **智能文本分块**
**概念 / Concept:** 将长文档分割成适合向量化的小块
**学习目标 / Learning Goals:**
- 理解 `chunk_size` 和 `chunk_overlap` 的影响
- 使用 `RecursiveCharacterTextSplitter` 进行语义分块
- 优化分块策略以保留上下文

**关键参数 / Key Parameters:**
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,      # 每块约200字符
    chunk_overlap=50     # 相邻块重叠50字符，防止语义断裂
)
```

**为什么需要分块？/ Why is chunking necessary?**
- 避免超过 Token 上限
- 提高检索精度
- 减少向量数据库大小

---

### **第五阶段：向量化与语义搜索 / Phase 5: Vectorization & Semantic Search**

#### 25_embeddings.ipynb 🔢 **嵌入向量生成**
**概念 / Concept:** 将文本转换为高维向量表示（Semantic Embeddings）
**学习目标 / Learning Goals:**
- 理解 `OpenAIEmbeddings` 的工作原理
- 掌握向量维度与模型的关系
- 对比不同嵌入模型的性能

**模型对比 / Model Comparison:**
```
text-embedding-3-small  → 1536 维，快速，适合简单应用
text-embedding-3-large  → 3072 维，精确，适合复杂任务
```

**代码示例 / Code Example:**
```python
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector = embeddings.embed_query("machine learning")  # 得到 3072 维向量
```

---

#### 26_semantic_search.ipynb 🔍 **向量相似度搜索**
**概念 / Concept:** 基于向量余弦距离的语义搜索
**学习目标 / Learning Goals:**
- 构建 Chroma 向量数据库
- 执行 Top-K 相似度搜索
- 理解向量空间中的"语义相似性"

**搜索流程 / Search Pipeline:**
```
查询文本 / Query Text
    ↓
转换为向量 / Convert to Vector
    ↓
计算相似度 / Calculate Similarity
    ↓
返回 Top-K 结果 / Return Top-K Results
```

---

### **第六阶段：RAG 检索增强生成 / Phase 6: RAG - Retrieval-Augmented Generation**

#### 27_RAG_PDF.ipynb 📚 **PDF 文档 RAG**
**概念 / Concept:** 结合向量检索和 LLM，从 PDF 文档中提取准确答案
**学习目标 / Learning Goals:**
- 理解完整的 RAG 管道
- 实现防幻觉的问答系统
- 处理知识文档库

**RAG 核心流程 / RAG Pipeline:**
```
用户问题 / User Question
    ↓
向量检索 / Vector Retrieval → Top-3 相关文档块
    ↓
格式化上下文 / Format Context
    ↓
LLM 生成答案 / LLM Generates Answer (仅从检索文档)
    ↓
防止幻觉 / Anti-Hallucination Check
```

**提示词设计 / Prompt Design:**
```python
template = """只根据以下上下文回答问题。如果文档中没有答案，直接说"我不知道"。

上下文: {context}
问题: {question}
"""
```

---

#### 28_RAG_WEB.ipynb 🌍 **网页内容 RAG**
**概念 / Concept:** 实时从互联网网页中检索和回答问题
**学习目标 / Learning Goals:**
- 集成 WebBaseLoader 进行动态网页加载
- 构建实时新闻问答系统
- 处理动态数据源

**应用场景 / Use Cases:**
- 实时新闻提问（"最新的 AI 进展是什么？"）
- 技术文档查询
- 竞争对手监控

---

### **第七阶段：高级链条与文档处理 / Phase 7: Advanced Chains**

#### 29_Document_chain.ipynb 📋 **文档内容提取链**
**概念 / Concept:** 使用 `create_stuff_documents_chain` 批量处理多个文档
**学习目标 / Learning Goals:**
- 理解 "Stuff" 策略（将所有文档内容直接注入 Prompt）
- 对比不同的文档合并策略
- 实现多文档分析

**三大文档合并策略 / Document Combination Strategies:**
```
1. Stuff       → 直接拼接所有文档（快速但受 Token 限制）
2. Map-Reduce  → 分别处理每个文档，再汇总结果
3. Refine      → 逐个处理，不断精化答案
```

---

#### 30_Retrival_chain.ipynb 🔗 **完整检索链**
**概念 / Concept:** 整合 Retriever 和 Document Chain 的完整系统
**学习目标 / Learning Goals:**
- 使用 `create_retrieval_chain` 工厂函数
- 实现端到端的问答流程
- 优化检索和生成的融合

**完整架构 / Complete Architecture:**
```
Query → Retriever → Documents → Combine Chain → LLM → Answer
   ↓
内部处理：向量相似度计算、文档排序、上下文拼接
```

---

### **第八阶段：工具与外部 API / Phase 8: Tools & External APIs**

#### 31_Wikipedia.ipynb 📖 **维基百科工具集成**
**概念 / Concept:** 将维基百科集成为 LangChain 的外部工具
**学习目标 / Learning Goals:**
- 使用 `WikipediaQueryRun` 工具
- 理解工具的元数据（name, description, args）
- 为后续 Agent 准备工具基础

**工具自检 / Tool Introspection:**
```python
tool = WikipediaQueryRun(...)
print(f"名称: {tool.name}")
print(f"描述: {tool.description}")
print(f"参数: {tool.args}")
```

---

#### 32_Travily.ipynb 🔎 **实时网络搜索**
**概念 / Concept:** 使用 Tavily 进行高质量的实时网络搜索
**学习目标 / Learning Goals:**
- 集成 `TavilySearchResults` 工具
- 获取最新的网络信息
- 为 Agent 提供实时查询能力

**优势 / Advantages:**
- ✅ 实时搜索结果
- ✅ 多个来源筛选
- ✅ 高相关性排序

---

#### 33_Yahoo_Finance.ipynb 💹 **财经数据工具**
**概念 / Concept:** 集成雅虎财经数据源
**学习目标 / Learning Goals:**
- 使用 `YahooFinanceNewsTool` 获取股票新闻
- 实现金融信息查询
- 构建智能投资助手基础

**可查询资产 / Queryable Assets:**
- 股票（NVDA, AMZN, GOOGL）
- 加密货币
- 指数基金

---

#### 34_Customized_Tool.ipynb 🛠️ **自定义工具开发**
**概念 / Concept:** 创建符合 LangChain 标准的自定义工具
**学习目标 / Learning Goals:**
- 使用 `@tool` 装饰器定义工具
- 编写清晰的文档字符串和类型注解
- 集成真实的 API 调用（如航班查询）

**关键代码模式 / Key Pattern:**
```python
from langchain_core.tools import tool

@tool
def get_flight_status(flight: str) -> str:
    """获取指定航班的实时状态、起飞时间和到达时间。
    
    格式要求：航班代码，例如 'EK524' 或 'UAL1'。
    """
    # 调用真实的航空公司 API...
    return f"Flight {flight} status: On-time..."
```

**三个必要要素 / Three Essential Elements:**
1. ✅ 清晰的函数签名 / Function signature
2. ✅ 完整的文档字符串 / Docstring
3. ✅ 正确的参数类型注解 / Type annotations

---

### **第九阶段：智能体与推理 / Phase 9: Agents & Reasoning**

#### 35_Agent_Search.ipynb 🤖 **基础智能体与搜索**
**概念 / Concept:** 创建能够自主思考、调用工具和迭代推理的人工智能代理
**学习目标 / Learning Goals:**
- 理解 ReAct（Reasoning + Acting）框架
- 使用 `create_tool_calling_agent` 构建智能体
- 集成工具调用和推理循环
- 实现对话记忆管理

**智能体核心循环 / Agent Core Loop:**
```
思考 / Thought → 判断是否需要工具 / Judge → 调用工具 / Act → 观察结果 / Observe
  ↓
再次思考 / Re-think...（循环直到解决问题）
```

**代码架构 / Code Architecture:**
```python
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor

# 工具箱
tools = [TavilySearchResults()]

# 创建智能体大脑
agent = create_tool_calling_agent(llm, tools, prompt)

# 启动执行引擎
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 执行
result = agent_executor.invoke({"input": "问题..."})
```

**记忆管理 / Memory Management:**
```python
from langchain_core.runnables.history import RunnableWithMessageHistory

agent_with_memory = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)
```

---

#### 36_REPL.ipynb 🔧 **Python 代码执行工具**
**概念 / Concept:** 让 AI 代理能够执行 Python 代码进行计算
**学习目标 / Learning Goals:**
- 使用 `PythonREPLTool` 安全执行 Python 代码
- 实现数学运算和数据处理
- 克服 LLM 的计算弱点

**应用场景 / Use Cases:**
- 复杂数学计算
- 数据分析和处理
- 代码验证

---

#### 37_flightagent.ipynb ✈️ **终极智能体：航班查询系统**
**概念 / Concept:** 融合所有前面知识点的完整系统应用
**学习目标 / Learning Goals:**
- 集成真实的 FlightAware API
- 构建多工具智能体
- 实现复杂的推理和决策

**完整架构 / Complete System Architecture:**
```
用户问题（例如：查询EK524的起飞时间）
    ↓
Agent 理解意图
    ↓
调用 get_flight_status 工具 (返回实时航班数据)
    ↓
可能调用 PythonREPLTool 进行时间计算
    ↓
综合多个源的数据，生成自然语言答案
```

**关键技术点 / Key Technical Points:**
- ✅ 工具调用的动态选择
- ✅ API 错误处理
- ✅ 时间计算和时区管理
- ✅ 上下文保持

---

### **其他重要文件 / Other Important Files**

#### 06_Few-shot_prompt_templates_demo.ipynb 🎓
**概念：** 通过示例学习（In-context Learning）
**核心思想：** 在 Prompt 中提供几个示例，帮助 LLM 理解任务模式

---

#### 07-09_ParsingModelOutput_demo.ipynb 🎨
**概念：** 多种输出解析策略
- Demo1: 简单字符串解析
- Demo2: 复杂 JSON 解析
- Demo3: 自定义格式解析

---

#### 10_Keylibraries_demo.ipynb 🔑
**概念：** LangChain 核心库的概览和对比

---

#### 11_debuging_langchain_demo.ipynb 🐛
**概念：** 链条调试技巧
- 使用 `verbose=True`
- 打印中间结果
- 分步调试

---

#### 12_StdOutCallbackHandler_demo.ipynb 📢
**概念：** 使用回调函数监控链的执行
- Token 计数
- 执行时间统计
- 自定义事件处理

---

#### test.ipynb 🧪
**概念：** 实验性演示代码

---

## 🏗️ 项目架构总览 / Project Architecture Overview

```
LangChain 学习项目
├─ 基础阶段 (01-05)
│  ├─ Chain 概念
│  ├─ Model I/O
│  └─ Prompt Engineering
│
├─ 高级链条 (13-18)
│  └─ LCEL 表达式语言
│
├─ 记忆管理 (19-21)
│  ├─ 短期记忆 (MessagesPlaceholder)
│  └─ 长期记忆 (数据库存储)
│
├─ 文档处理 (22-24)
│  ├─ 加载 (PDF, Web)
│  └─ 切分 (Chunking)
│
├─ 向量与搜索 (25-26)
│  ├─ Embeddings
│  └─ Semantic Search
│
├─ RAG 系统 (27-30)
│  ├─ RAG with 静态文档
│  └─ RAG with 动态网页
│
├─ 工具集成 (31-34)
│  ├─ 维基百科
│  ├─ 网络搜索
│  ├─ 金融数据
│  └─ 自定义工具
│
└─ 智能体 (35-37)
   ├─ 基础 Agent
   ├─ Agent + 工具
   └─ 完整系统应用
```

---

## 🔑 核心概念速查表 / Quick Reference

### LangChain 的 5 大核心模块

| 模块 | 用途 | 关键类 |
|------|-----|--------|
| **Model I/O** | 与 LLM 交互 | ChatOpenAI, PromptTemplate, OutputParser |
| **Retrieval** | 检索文档 | Loader, Splitter, Retriever, VectorStore |
| **Chains** | 组合工作流 | LLMChain, LCEL (Pipe \|) |
| **Agents** | 自主推理与工具调用 | create_tool_calling_agent, AgentExecutor |
| **Memory** | 管理对话历史 | ChatMessageHistory, RunnableWithMessageHistory |

---

## 💡 常见工作流模式 / Common Workflow Patterns

### 模式 1: 简单问答
```python
chain = prompt | llm | output_parser
response = chain.invoke({"question": "..."})
```

### 模式 2: RAG 文档问答
```python
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt | llm | StrOutputParser()
)
response = rag_chain.invoke("用户问题")
```

### 模式 3: 智能体工具调用
```python
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
result = agent_executor.invoke({"input": "问题"})
```

### 模式 4: 带记忆的对话
```python
agent_with_memory = RunnableWithMessageHistory(agent_executor, get_session_history)
result = agent_with_memory.invoke(
    {"input": "问题"},
    config={"configurable": {"session_id": "user_123"}}
)
```

---

## 📊 学习时间规划 / Learning Timeline

| 阶段 | 文件 | 预计时间 | 难度 |
|------|-----|---------|------|
| 基础 | 01-05 | 2-3 小时 | ⭐ |
| LCEL | 13-18 | 3-4 小时 | ⭐⭐ |
| 记忆 | 19-21 | 1-2 小时 | ⭐⭐ |
| 文档 | 22-24 | 2 小时 | ⭐⭐ |
| 向量 | 25-26 | 2 小时 | ⭐⭐ |
| RAG | 27-30 | 3-4 小时 | ⭐⭐⭐ |
| 工具 | 31-34 | 2-3 小时 | ⭐⭐⭐ |
| 智能体 | 35-37 | 4-5 小时 | ⭐⭐⭐⭐ |
| **总计** | | **19-23 小时** | |

---

## 🎯 推荐学习路径 / Recommended Learning Path

### 初学者路径 / Beginner Path
```
01 → 02 → 05 → 13 → 22 → 24 → 25 → 26 → 27
基础  Model  Prompt  LCEL  加载  分块  向量  搜索  RAG
```
**时间：** 6-8 小时  
**目标：** 理解 LangChain 基本概念和 RAG 完整流程

---

### 进阶路径 / Intermediate Path
```
基础路径 → 19 → 20 → 28 → 29 → 30 → 31 → 32
      记忆  配置  Web-RAG  链   检索  维基  搜索
```
**时间：** 12-15 小时  
**目标：** 掌握高级特性和多工具集成

---

### 专家路径 / Expert Path
```
进阶路径 → 33 → 34 → 35 → 36 → 37
       金融  自定义  搜索Agent  代码执行  完整应用
```
**时间：** 20+ 小时  
**目标：** 构建生产级的复杂系统

---

## 🚦 运行代码的注意事项 / Important Notes

### 环境变量配置 (.env file)
```
# 必需 / Required
OPENAI_API_KEY=sk-...

# 可选 / Optional
TAVILY_API_KEY=tvly-...  # 用于网络搜索 / For web search
FLIGHTAWARE_API_KEY=...  # 用于航班查询 / For flight queries
```

### 常见问题解决 / Troubleshooting

**❌ 问题：API Key 未找到**
```
解决：确保 .env 文件在项目根目录，且使用 load_dotenv(override=True)
Fix: Ensure .env is in project root and use load_dotenv(override=True)
```

**❌ 问题：PDF 加载失败**
```
解决：安装 pip install pdf2image pdfplumber
Fix: Install pip install pdf2image pdfplumber
```

**❌ 问题：向量库超过 Token 限制**
```
解决：减小 chunk_size (如 200 改为 100) 或 upgrade 模型
Fix: Reduce chunk_size (e.g., 200 to 100) or upgrade model
```

---

## 📚 相关资源 / Related Resources

- **官方文档：** https://python.langchain.com/
- **API 参考：** https://api.python.langchain.com/
- **社区讨论：** https://github.com/langchain-ai/langchain
- **Cookbook：** https://github.com/langchain-ai/langchain-cookbook

---

## 🎓 学完后的下一步 / Next Steps After Learning

1. **构建自己的项目**
   - 创建企业内部知识库问答系统
   - 构建个人AI助手
   - 开发垂直领域的应用

2. **深化学习**
   - 研究 LLM 微调技术
   - 学习向量数据库优化
   - 研读论文：RAG, In-context Learning 等

3. **性能优化**
   - 缓存优化（避免重复调用）
   - 并发处理
   - 成本控制

4. **部署上线**
   - 使用 FastAPI 构建 API
   - Docker 容器化
   - 云平台部署（AWS, Azure, GCP）

---

## 📝 许可证 / License

本项目所有代码均为学习目的，遵循 MIT License。

---

## 👨‍💻 贡献指南 / Contributing

欢迎提交 Issue 和 Pull Request！

---

## 📧 联系方式 / Contact

有问题？欢迎提出 Issue 或讨论！

---

**最后更新 / Last Updated:** 2026-03-04  
**文档版本 / Documentation Version:** 1.0  
**支持语言 / Languages Supported:** 中文 / English

---

## 📈 进度追踪 / Progress Tracking

学习完毕请打勾：

- [ ] 01_first_chain.ipynb ✓
- [ ] 02_model_io_chain.ipynb ✓
- [ ] 03_model_io_parser.ipynb ✓
- [ ] 04_messages_in_chatmodel_demo.ipynb ✓
- [ ] 05_Prompt_templates_demo.ipynb ✓
- [ ] 06_Few-shot_prompt_templates_demo.ipynb ✓
- [ ] 07_ParsingModelOutput_demo1.ipynb ✓
- [ ] 08_ParsingModelOutput_demo2.ipynb ✓
- [ ] 09_ParsingModelOutput_demo3.ipynb ✓
- [ ] 10_Keylibraries_demo.ipynb ✓
- [ ] 11_debuging_langchain_demo.ipynb ✓
- [ ] 12_StdOutCallbackHandler_demo.ipynb ✓
- [ ] 13_LCEL_demo1.ipynb ✓
- [ ] 14_LCEL_demo2.ipynb ✓
- [ ] 15_LCEL_demo3.ipynb ✓
- [ ] 16_LCEL_demo4.ipynb ✓
- [ ] 17_LCEL_demo5.ipynb ✓
- [ ] 18_LCEL_demo6.ipynb ✓
- [ ] 19_short-term_memory.ipynb ✓
- [ ] 20_contigurable_parameters.ipynb ✓
- [ ] 21_Long-term_memory.ipynb ✓
- [ ] 22_loading_PDFs.ipynb ✓
- [ ] 23_loading-webpages.ipynb ✓
- [ ] 24_chunking_documents.ipynb ✓
- [ ] 25_embeddings.ipynb ✓
- [ ] 26_semantic_search.ipynb ✓
- [ ] 27_RAG_PDF.ipynb ✓
- [ ] 28_RAG_WEB.ipynb ✓
- [ ] 29_Document_chain.ipynb ✓
- [ ] 30_Retrival_chain.ipynb ✓
- [ ] 31_Wikipedia.ipynb ✓
- [ ] 32_Travily.ipynb ✓
- [ ] 33_Yahoo_Finance.ipynb ✓
- [ ] 34_Customized_Tool.ipynb ✓
- [ ] 35_Agent_Search.ipynb ✓
- [ ] 36_REPL.ipynb ✓
- [ ] 37_flightagent.ipynb ✓

---

**祝你学习顺利! Happy Learning! 🎉**
