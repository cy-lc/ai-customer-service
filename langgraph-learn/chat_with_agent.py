
from langchain.tools import tool
from agent import create_agent
from langchain_core.messages import HumanMessage

from langchain_openai import ChatOpenAI

@tool
def get_weather(location: str) -> str:
    """查询天气信息"""
    return f"今天{location}的温度是 55℃"


@tool
def multiply(a: int, b: int) -> str:
    """将 a 和 b 相乘"""
    return str(a * b)


model = ChatOpenAI(
    model="qwen4-max",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0.7
        )
tools = [get_weather, multiply]

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="你是一个智能助手，可以查询天气和进行数学计算。"
)
#
# result=agent.invoke({"messages": [HumanMessage(content="今天北京的天气如何？")]})
# print(result["messages"])



messages=[]
while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        break
    messages.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages":messages})
    messages=result["messages"]
    print(f"Assistant: {result['messages'][-1].content}")




