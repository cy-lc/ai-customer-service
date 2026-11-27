from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# 1. 定义状态
class PackageState(TypedDict):
    package_id: str  # 包裹单号
    is_damaged: bool  # 是否损坏（True=损坏，False=完好）

    inspection_note: str  # 验货备注
    final_action: str  # 最终操作（签收/拒收）


# 2. 节点1：验货
def inspect(state: PackageState) -> PackageState:
    pkg_id = state["package_id"]
    # 模拟验货：单号含"9"的算损坏
    damaged = "9" in pkg_id

    if damaged:
        state["is_damaged"] = True
        state["inspection_note"] = f"⚠️ 包裹{pkg_id}外包装破损"
    else:
        state["is_damaged"] = False
        state["inspection_note"] = f"✅ 包裹{pkg_id}完好无损"
    return state


# 3. 节点2：签收
def sign(state: PackageState) -> PackageState:
    if state["is_damaged"]:
        state["final_action"] = f"❌ 拒收！{state['inspection_note']}"
    else:
        state["final_action"] = f"✅ 签收成功！{state['inspection_note']}"
    return state


# 4. 构建图
builder = StateGraph(PackageState)
builder.add_node("inspect", inspect)
builder.add_node("sign", sign)

builder.add_edge(START, "inspect")
builder.add_edge("inspect", "sign")
builder.add_edge("sign", END)

graph = builder.compile()

from IPython.display import Image, display
display(Image(graph.get_graph(xray=True).draw_mermaid_png()))

# 测试 1：完好的包裹
result1 = graph.invoke({"package_id": "PKG123"})
print(f"包裹ID: {result1['package_id']}")
print(f"验货结果: {result1['inspection_note']}")
print(f"最终操作: {result1['final_action']}")

print("\n" + "=" * 40)