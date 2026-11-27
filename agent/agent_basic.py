from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool


user_query="今天 北京的天气怎么样？"
#1.创建模型客户端
llm=ChatTongyi(model="qwen-max")
messages=[
    ("system", "你是一个天气助手"),
    ("user", f"{user_query}")
]
#2.给模型添加工具
@tool
def get_weather(location: str):
    """
    获取某个位置的天气
    :param location: str
    :return: str
    """
    return f"{location}的天气是80度，请避暑。"

tools=[get_weather]
model_with_tools=llm.bind_tools(tools=tools)

result=model_with_tools.invoke(user_query)
print(result)
print("\n\n\n")



tool_map={tool.name:tool for tool in tools}
print(tools)
print("\n\n\n")
print(tool_map)
if result.tool_calls:
    messages.append(result)
    for tool_call in result.tool_calls:
        tool_name=tool_call.get("name")#工具名字
        tool_args=tool_call.get("args")#工具参数
        tool_id=tool_call.get("id")#工具id
        tool_func=tool_map.get(tool_name)
        if tool_func:
           try:
               tool_result=tool_func.invoke(tool_args)
               print(f"工具 '{tool_name}' 调用结果: {tool_result}")
               tool_messages=ToolMessage(
                   content=tool_result,
                   tool_call_id=tool_id
               )
               messages.append(tool_messages)
           except Exception as e:
               print(f"调用工具 '{tool_name}' 失败: {e}")
               tool_message = ToolMessage(
                   content=f"工具调用失败: {str(e)}",
                   tool_call_id=tool_id
               )
               messages.append(tool_message)
        else:
           print(f"未找到工具: {tool_name}")
           tool_messages = ToolMessage(
               content=f"未找到工具: {tool_name}",
               tool_call_id=tool_id
           )
           messages.append(tool_messages)
else:
    print("没有需要调用的工具")
    print(result.content)
for message in messages:
    print(f"{type(message)},         {message}")
print("\n\n\n")
result=model_with_tools.invoke(messages)
print(result)





