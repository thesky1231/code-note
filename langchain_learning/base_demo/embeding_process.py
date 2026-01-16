# 从pdf_process里引用splits(切分好的块)
from pdf_process import splits
import os
import shutil
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

if os.path.exists("./db"):
    shutil.rmtree("./db")

# 聘请翻译官
embeddings = OllamaEmbeddings(model="nomic-embed-text")

print("正在初始化向量数据库...")

# 存入向量数据库
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory="./db"
)


print("恭喜！数据已成功存入本地向量数据库！")
print("你现在可以去你的代码文件夹看看，是不是多了一个叫 'db' 的文件夹？")