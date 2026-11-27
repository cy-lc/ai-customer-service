#狭义模型
# from langchain_community.llms.tongyi import Tongyi
# llm =Tongyi(model="qwen-max")
# ai_response = llm.invoke("Hello, how are you?")
# print(ai_response)


# #聊天模型
# from langchain_community.chat_models import ChatTongyi
# from langchain_core.messages import SystemMessage, HumanMessage
#
# llm = ChatTongyi(model="qwen-max", streaming=True)
# chat_history=[
#     SystemMessage("You are a helpful assistant."),
#     HumanMessage("尧怎么读")
# ]
# result=llm.stream(chat_history)
# for chunk in result:
#     print(chunk.content,end="", flush=True)


#嵌入模型
from langchain_community.embeddings import DashScopeEmbeddings
embeddings = DashScopeEmbeddings()
text = ["陈尧帅哥","陈尧是帅哥","ai应用开发"]
embedding = embeddings.embed_documents(text)
print(embedding)
#计算欧氏距离
import numpy as np
def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

distance = euclidean_distance(np.array(embedding[0]), np.array(embedding[1])) # 计算两个向量之间的欧氏距离
print(distance)








