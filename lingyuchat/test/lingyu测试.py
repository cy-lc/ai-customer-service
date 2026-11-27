import os
from dotenv import load_dotenv
from core.chat_service import ChatService
from core.protocl import ChatRequest
import uuid

load_dotenv()

# 创建测试请求
request = ChatRequest(
    user_id="test_user",
    chat_session_id="test_session",
    trace_id=str(uuid.uuid4()),
    user_input="我的快递到哪了?我的订单号是7856757536124",
    api_key=os.environ["DASHSCOPE_API_KEY"])

print(f"测试请求: {request}")
try:
    chat_service = ChatService()
    response = chat_service.handle_chat(request)
    print(f"测试响应: {response}")
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"测试失败: {e}")