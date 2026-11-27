from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import SystemMessage, HumanMessage
class MultiTurnChat:
     def __init__(self, model: str, system_prompt: str=None):
         self.llm=ChatTongyi(model=model, streaming=True)
         self.chat_history=[]
         if system_prompt:
             self.chat_history.append("system",system_prompt)
     def add_user_message(self,content:str):
         self.chat_history.append(("human",content))
     def add_ai_message(self,fullreply:str):
         self.chat_history.append(("ai",fullreply))
     def send(self,user_message):
         self.add_user_message(user_message)
         stream=self.llm.stream(self.chat_history)
         fullreply=""
         for chunk in stream:
             if chunk.content:
                 fullreply+=chunk.content
                 yield chunk.content
         self.add_ai_message(fullreply)
if __name__=="__main__":
    chat=MultiTurnChat(model="qwen-max")
    print("欢迎使用多轮对话模式，输入exit或quit退出")
while True:
    user_input=input("用户：")

    for chunk in chat.send(user_input):
        if user_input.strip() in ["exit","quit"]:
            break
        if not user_input.strip():
            print("请不要输入空格")
            continue
        print(chunk,end="",flush=True)
    print()














