from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool


#1.创建tool
@tool
def get_goods_info_by_id(goods_id: int) -> str | None:
    """
    根据商品goods_id去查询商品信息
    :param goods_id: 商品id
    :return: 查询到的商品信息，没查询到就返回空
    """
    goods_info = {
        1: "爱疯手机",
        2: "华为电脑"
    }
    if goods_id not in goods_info:
        print(f"id为{goods_id}的商品不存在")
        return None
    goods = goods_info[goods_id]
    print(f"id为{goods_id}的商品为: {goods}")
    return goods

#2. 创建agent
tools=[get_goods_info_by_id]
agent=create_agent(
    model=ChatTongyi(model="qwen-max"),
    tools=tools,
    system_prompt="你是一个商品查询助手",
 )
user_input="查询id为1的商品信息"
result=agent.invoke(
     {"messages":[{"role":"user","content":user_input}]}

 )
print(type(result))
print("\n\n")
print(result["messages"][-1].content)

