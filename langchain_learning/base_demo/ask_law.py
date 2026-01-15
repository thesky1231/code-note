from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
# 导入 LangChain 的核心链构建工具
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# === 1. 准备模型 ===
# 必须和你存数据时用的模型一模一样，否则读不懂
embeddings = OllamaEmbeddings(model="qwen2.5:7b")
llm = ChatOllama(model="qwen2.5:7b", temperature=0)

# === 2. 加载数据库 ===
# 注意：如果你现在的终端路径在 src 下，且 db 也在 src 下，这里用 "./db" 没问题
# 否则可能会报错说找不到数据库
vectorstore = Chroma(
    persist_directory="./db", 
    embedding_function=embeddings
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# === 3. 定制你的“提问模板” (Prompt) ===
# 这就是新写法的最大优势，你可以教 AI 怎么说话
prompt = ChatPromptTemplate.from_template("""
你是一个专业的法律顾问助手。
请根据下面的【法律条文】来回答用户的【问题】。
如果你在条文里找不到答案，请直接说“法律条文中未提及”，不要瞎编。

【法律条文】：
{context}

【问题】：
{input}
""")

# === 4. 搭建流水线 ===
# 步骤A：创建一个“能读懂文档并回答”的链
combine_docs_chain = create_stuff_documents_chain(llm, prompt)

# 步骤B：创建一个“先检索再回答”的完整链
# 这里的 retriever 负责找书，combine_docs_chain 负责读内容并回答
rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

# === 5. 开始考试！ ===
question = "故意杀人罪怎么判刑？"
print(f"🕵️ 正在咨询 AI 律师：{question}")

# 运行链
result = rag_chain.invoke({"input": question})

print("\n=== 📜 AI 的法律意见 ===")
print(result["answer"])

# 🎁 彩蛋：看看它参考了哪几段话
print("\n=== 📚 参考来源 ===")
for i, doc in enumerate(result["context"]):
    print(f"[来源 {i+1}] {doc.page_content[:50]}...") # 只打印前50个字预览