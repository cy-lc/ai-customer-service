from langchain_core.messages import HumanMessage, ToolMessage
from typing import List, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage

# 1.定义工具和模型
from langchain.tools import tool

model=ChatOpenAI(
    model="qwen4-max",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0.7
        )

@tool
def get_weather(location: str) -> str:
    """
    查询天气信息
    :param location: 地理位置
    :return: 天气情况
    """
    return f"今天{location}的温度是 200℃"

# 定义工具
@tool
def multiply(a: int, b: int) -> int:
    """
    将`a`和`b`相乘。
    :param a: 第一个整数
    :param b: 第二个整数
    :return: 相加的结果
    """
    return a * b

tools = [get_weather, multiply]
model_with_tools = model.bind_tools(tools=tools)
tools_by_name = {tool.name: tool for tool in tools}
print(tools_by_name)

# 2. 定义状态

class ReActAgentState(TypedDict):
    messages: List[BaseMessage]
    llm_calls: int

# 3. 定义节点


def llm_call(state: ReActAgentState) -> ReActAgentState:
    """LLM决定是否调用工具"""
    msgs = [SystemMessage('你是一个有用的助手。')] + state["messages"]
    ai_message = model_with_tools.invoke(msgs)
    state['messages'] = state["messages"] + [ai_message]
    state['llm_calls'] += 1
    return state

def tool_call(state: ReActAgentState) -> ReActAgentState:
    """执行工具调用"""
    last_message = state["messages"][-1]
    tool_calls = last_message.tool_calls
    for tool_call in tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_result = tools_by_name[tool_name].invoke(tool_args)
        state['messages'].append(
            ToolMessage(
                content=tool_result,
                tool_call_id=tool_call["id"]
            )
        )
    state['llm_calls'] += 1
    return state


# 4. 构建图
builder = StateGraph(ReActAgentState)
builder.add_node("llm_call", llm_call)
builder.add_node("tool_call", tool_call)

builder.add_edge(START, "llm_call")

# 条件边：判断是否需要调用工具
def router(state: ReActAgentState) -> str:
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tool_call"
    return END

builder.add_conditional_edges(
    "llm_call",
    router,
    {
        "tool_call": "tool_call",
        END: END
    }
)

builder.add_edge("tool_call", "llm_call")  # 工具调用后回到LLM
graph = builder.compile()



print("=" * 50)
print("🤖 ReAct Agent 测试")
print("=" * 50)
# 测试1：乘法
initial_state = {
    "messages": [HumanMessage(content="3乘以4等于多少？")],
    "llm_calls": 0
}
result = graph.invoke(initial_state)
# print(result)
print("\n✅ 最终结果:")
for msg in result["messages"]:
    msg_type = type(msg).__name__
    # 打印消息内容
    if hasattr(msg, "content") and msg.content:
        print(f"{msg_type}: {msg.content}")
    # 打印 tool_calls
    if hasattr(msg, "tool_calls") and msg.tool_calls:
        for tc in msg.tool_calls:
            print(f"AI → 调用工具: {tc['name']}({tc['args']})")
print(f"\n📊 LLM调用次数: {result['llm_calls']}")

