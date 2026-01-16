from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama


# 准备提示词模板
prompt = ChatPromptTemplate.from_template("请把这句话翻译成英文：{text}")

# 选择模型
model = ChatOllama(model="qwen2.5:7b", temperature=1)

# 将输出只保留content部分
parser = StrOutputParser()

chain = prompt | model | parser
# chain = prompt | model

print("正在思考...")

# 这里不是agent，只是单纯的一问一答，所以只需要输入prompt里面的填空参数即可
result = chain.invoke({"text": "我爱学习人工智能"})
print(result)