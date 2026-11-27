from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Optional, Annotated
from langchain_core.messages.base import BaseMessage
from langchain_core.messages import SystemMessage, ToolMessage, HumanMessage, AIMessage
from langchain_core.language_models import BaseLanguageModel
from langchain.tools import BaseTool
import operator
# agent.py 里面的状态类
class ReActAgentState(TypedDict):
    # messages: List[BaseMessage]
    messages: Annotated[List[BaseMessage],operator.add]

def create_agent(
    model: BaseLanguageModel,
    tools: List[BaseTool],
    system_prompt: str = "你是一个有用的助手。"
):
    """
    创建一个 ReAct Agent 图
    Args:
        model: 大语言模型实例
        tools: 工具列表
        system_prompt: 系统提示词
    Returns:
        编译好的StateGraph实例
    """
# 绑定工具到模型
    model_with_tools = model.bind_tools(tools)
    tools_by_name = {tool.name: tool for tool in tools}
    # def llm_call(state: ReActAgentState) -> ReActAgentState:
    #     """LLM决定是否调用工具"""
    #     msgs = [SystemMessage(system_prompt)] + state["messages"]
    #     ai_message = model_with_tools.invoke(msgs)
    #     state['messages'] = state["messages"] + [ai_message]
    #     return state

    def llm_call(state: ReActAgentState) -> ReActAgentState:
        """LLM决定是否调用工具"""
        msgs = [SystemMessage(system_prompt)] + state["messages"]
        ai_message = model_with_tools.invoke(msgs)
        state['messages'] = state["messages"] + [ai_message]
        return {"messages": [ai_message]}
    #
    # def tool_call(state: ReActAgentState) -> ReActAgentState:
    #     """执行工具调用"""
    #     last_message = state["messages"][-1]
    #     tool_calls = last_message.tool_calls
    #     for tool_call in tool_calls:
    #         tool_name = tool_call["name"]
    #         tool_args = tool_call["args"]
    #         tool_result = tools_by_name[tool_name].invoke(tool_args)
    #         state['messages'].append(
    #             ToolMessage(
    #                 content=str(tool_result),
    #                 tool_call_id=tool_call["id"]
    #             )
    #         )
    #     return state

    def tool_call(state: ReActAgentState) -> ReActAgentState:
        """执行工具调用"""
        last_message = state["messages"][-1]
        tool_calls = last_message.tool_calls
        tool_messages=[]
        for tool_call in tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_result = tools_by_name[tool_name].invoke(tool_args)
            tool_messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"]
                )
            )
        return {"messages": tool_messages}
    # 定义路由函数
    def router(state: ReActAgentState) -> str:
        """判断是否需要调用工具"""
        last_message = state["messages"][-1]
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tool_call"
        return "end"

    # 构建图
    builder = StateGraph(ReActAgentState)
    builder.add_node("llm_calls", llm_call)
    builder.add_node("tool_calls", tool_call)
    builder.add_edge(START, "llm_calls")
    builder.add_conditional_edges(
        "llm_calls",
        router,
        {
            "tool_call": "tool_calls",
            "end": END
        }
    )
    builder.add_edge("tool_calls", "llm_calls")
    return builder.compile()

