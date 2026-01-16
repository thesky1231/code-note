import chromadb
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 准备向量数据库
DB_PATH = "./db"
# 设置翻译官，需要和将文本转化为向量的翻译官一致，因为要确保互相转换后意思改变不大
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 创建一个数据库管理员通道
client = chromadb.PersistentClient(path=DB_PATH)


vectorstore = Chroma(
    client=client,
    embedding_function=embeddings
)

# 构建巡回机器， "k"表示top-k
retriever = vectorstore.as_retriever(search_kwargs={"k" : 3})

# 准备prompt模板：
template = """
你是一个法律助手。请根据以下参考资料回答问题：

【参考资料】：
{context}

【问题】：
{question}
"""

# 设置prompt：
prompt = ChatPromptTemplate.from_template(template)

model = ChatOllama(model="qwen2.5:7b", temperature=0)


# 定义一个处理巡回文件列表的函数，拼接成可以放在prompt里的样子
def format_docs(docs):
    return "\n\n:".join([doc.page_content for doc in docs])


# 构建数据传输链
rag_chain = (
    # 并行分发
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)
# for i, doc in enumerate(retriever.invoke("故意杀人怎么判？")):
#     print(f"{i + 1}: {doc}")

print("AI 正在检索并生成...")

for chunk in rag_chain.stream("你的知识库里有什么罪？"):
    # flush参数表示强制刷新缓冲区，也就是输出字
    print(chunk, end="", flush=True)


