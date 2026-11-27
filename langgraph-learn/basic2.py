from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from typing import TypedDict

# 1. 定义状态：整个graph流通的数据结构
class CalculatorState(TypedDict):
    num1: float      # 第一个数字
    num2: float      # 第二个数字
    operator: str    # 运算符 + - * /
    result: float    # 计算结果

# 2. 节点函数：接收state，处理后返回新state
def printer(state: CalculatorState) -> CalculatorState:
    """根据操作符执行计算"""
    num1 = state["num1"]
    num2 = state["num2"]
    operator = state["operator"]
    print(f"准备计算 {num1} {operator} {num2}")
    return state

def add(state: CalculatorState) -> CalculatorState:
    """执行加法"""
    result = state["num1"] + state["num2"]
    state["result"] = result
    print(f"计算结果 {result}")
    return state

def subtract(state: CalculatorState) -> CalculatorState:
    """执行减法"""
    result = state["num1"] - state["num2"]
    state["result"] = result
    print(f"计算结果 {result}")
    return state
# 定义 printer 节点的条件边
def router(state: CalculatorState) -> str:
    return "add_operation" if state['operator'] == "+" else "sub_operation"
builder = StateGraph(CalculatorState)
builder.add_node("printer", printer)
builder.add_node("add", add)
builder.add_node("subtract", subtract)

builder.add_edge(START, "printer")
builder.add_edge("add", END)
builder.add_edge("subtract", END)
builder.add_conditional_edges(
    "printer",  # 给谁加条件边
    router,
    {
        "add_operation": "add",
        "sub_operation": "subtract"
    }
)

graph = builder.compile()
# from IPython.display import Image, display
# display(Image(graph.get_graph(xray=True).draw_mermaid_png()))
graph.invoke({"num1": 10, "num2": 5, "operator": "+"})




