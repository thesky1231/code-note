from langchain.agents import create_agent
from langchain_ollama import ChatOllama


def get_weather(city: str) -> str:
    """这个工具是用来查询天气的"""  
    # 这里是文档字符串（docstring），是会加载进内存的
    # docstring必须是静态的 fail: f"""{city}"""
    return f"{city}天气是晴天。"

llm = ChatOllama(model="qwen2.5:7b", temperature=0.2)

agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="你是一个助理"
)

# invoke()传入和返回的都是一张agent_status,也就是一张表
result = agent.invoke(
    {"messages": [{"role": "user", "content": "北京的天气怎么样？"}]}
)
print(result["messages"][-1].content)