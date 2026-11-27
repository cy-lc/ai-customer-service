

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi




async def main():
    # 1. 创建客户端
    client = MultiServerMCPClient(
        {
            "weather": {
                "transport": "stdio",  # 子进程标准输入输出通信，和mcp.run(transport="stdio")对应
                "command": "python",
                # 启动weather这个MCP服务脚本的绝对路径
                "args": ["C:\\Users\\30133\\PycharmProjects\\WelcomeScreen\\study\\agent\\mcp\\mcp_server.py"],
            }
        }

    )
    tools=await client.get_tools()
    #3. 创建agent
    agent = create_agent(
    model=ChatTongyi(model="qwen-max"),
    tools=tools,
    system_prompt="你是一个助手,可以调用工具帮助用户解决问题"
    )
    result=await agent.ainvoke(
        {"messages": [{"role": "user", "content": "查询天气"}]}
    )
    print(result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
