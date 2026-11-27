

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

from langchain_openai import ChatOpenAI




async def main():
    # 1. 创建客户端
    client = MultiServerMCPClient(
        {
            "weather": {
                "transport": "stdio",  # 子进程标准输入输出通信，和mcp.run(transport="stdio")对应
                "command": "python",
                # 启动weather这个MCP服务脚本的绝对路径
                "args": ["C:\\Users\\30133\\PycharmProjects\\WelcomeScreen\\study\\agent\\mcp\\mcp_server.py"],
            },
            "database": {
                "transport": "stdio",  # 子进程标准输入输出通信，和mcp.run(transport="stdio")对应
                "command": "python",
                # 启动weather这个MCP服务脚本的绝对路径
                "args": ["C:\\Users\\30133\\PycharmProjects\\WelcomeScreen\\study\\agent\\mcp\\database.py"],
            }
        }

    )
    tools=await client.get_tools()
    #3. 创建agent
    agent = create_agent(
    model=ChatOpenAI(
    model="qwen4-max",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0.7
        ),
        tools=tools,
        system_prompt="你是一个助手,可以调用工具帮助用户解决问题"
    )
    result=await agent.ainvoke(
        {"messages": [{"role": "user", "content": "小米手机价格"}]}
    )
    print(result)
    print(result['messages'][-1].content)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
""""
{'messages': [HumanMessage(content='查询习水天气', additional_kwargs={}, response_metadata={}, id='84598e49-dbb7-4c42-9039-4992c2b350ba'),
 AIMessage(content='', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 50, 'prompt_tokens': 193, 'total_tokens': 243, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 22, 'rejected_prediction_tokens': None, 'text_tokens': None}, 'prompt_tokens_details': {'audio_tokens': None, 'cache_write_tokens': None, 'cached_tokens': 0, 'image_tokens': None, 'text_tokens': 193}}, 'model_provider': 'openai', 'model_name': 'qwen4-max', 'system_fingerprint': None, 'id': 'chatcmpl-38d98382-6532-9f64-8a20-2a1b4e1a8b5f', 'finish_reason': 'tool_calls', 'logprobs': None, 'normalized_finish_reason': 'tool_call'}, id='lc_run--01a20352-f789-74c4-8fec-c71c78aca03e-0', tool_calls=[{'name': 'get_weather', 'args': {'city': '习水'}, 'id': 'call_479e476b1f0b4d7baf19de5b', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 193, 'output_tokens': 50, 'total_tokens': 243, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 22}}),
  ToolMessage(content=[{'type': 'text', 'text': '习水天气100°.', 'id': 'lc_55eb3912-02a1-4ead-9018-6764d1c1ec13'}], name='get_weather', id='37301a37-3d54-49b7-9d8f-523a601d82d9', tool_call_id='call_479e476b1f0b4d7baf19de5b'), 
  AIMessage(content='根据查询结果,习水当前天气为 **100°**(若为华氏度,约相当于 37.8°C,天气较为炎热)。\n\n建议您注意防暑降温、多补充水分。如需了解更详细的天气信息(如湿度、风力、未来几天预报等),请告诉我。', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 120, 'prompt_tokens': 239, 'total_tokens': 359, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 54, 'rejected_prediction_tokens': None, 'text_tokens': None}, 'prompt_tokens_details': {'audio_tokens': None, 'cache_write_tokens': None, 'cached_tokens': 0, 'image_tokens': None, 'text_tokens': 239}}, 'model_provider': 'openai', 'model_name': 'qwen4-max', 'system_fingerprint': None, 'id': 'chatcmpl-11f6f188-67db-99c1-bc98-23acb797a35e', 'finish_reason': 'stop', 'logprobs': None, 'normalized_finish_reason': 'stop'}, id='lc_run--01a20353-07f8-72b8-8c1b-54c0fe470993-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 239, 'output_tokens': 120, 'total_tokens': 359, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 54}})]}

"""
