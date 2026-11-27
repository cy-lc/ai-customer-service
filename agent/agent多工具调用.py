from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool



# 准备数据
product_db = {
    "iPhone": {"id": 101, "price": 5999},
    "MacBook": {"id": 102, "price": 12999},
    "小米手机": {"id": 103, "price": 3999},
}

# 2.2. 工具A：根据名称获取ID
@tool(description="根据商品名称获取对应的商品ID")
def get_product_id_by_name(name: str) -> int | None:
    """输入商品名称（如'iPhone'），返回商品ID"""
    name_lower = name.lower()
    for prod_name, info in product_db.items():
        if prod_name.lower() == name_lower:
            print(f"[工具A] 商品 '{name}' 的 ID 是 {info['id']}")
            return info['id']
    print(f"[工具A] 未找到商品 '{name}'")
    return None

# 2.3. 工具B：根据ID获取价格
@tool(description="根据商品ID查询商品价格")
def get_product_price_by_id(product_id: int) -> str | None:
    """输入商品ID，返回价格字符串"""
    for prod_name, info in product_db.items():
        if info['id'] == product_id:
            price = info['price']
            print(f"[工具B] ID {product_id} 的商品 '{prod_name}' 价格为 {price} 元")
            return f"{prod_name} 的价格是 {price} 元"
    print(f"[工具B] 未找到 ID {product_id} 对应的商品")
    return None
agent = create_agent(
    ChatTongyi(model="qwen-max"),
    tools=[get_product_id_by_name, get_product_price_by_id],
    system_prompt="你是一个商品价格查询助手,获取商品价格",
)
user_input="我想知道小米手机价格"
result = agent.invoke({
    "messages": [{"role": "user", "content": user_input}]
})
print(result["messages"][-1].content)




