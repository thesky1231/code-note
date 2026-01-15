from langchain_ollama import ChatOllama


# cmd中用"ollama list"命令查看ollama下载了哪些模型
model = "qwen2.5:7b"
# temperature 可以理解为疯癫指数
llm = ChatOllama(model=model, temperature=0)

problem = "请用中文给我讲一个程序员笑话。"

# 对于单次对话（也就是简单的一问一答），是可以直接用字符串当参数的，但是agent就需要一张表，因为需要知道前因后果。
response = llm.invoke(problem)
print(f"大模型正在思考：{problem}")
print(response.content)
