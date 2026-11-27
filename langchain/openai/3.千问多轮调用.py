from openai import OpenAI
import os
class Multiturnchat:
    def __init__(self, base_url:str,model:str,system_prompt:str=None):
        self.client=OpenAI(base_url=base_url)
        self.model = model
        self.system_prompt = system_prompt
        self.chat_history = []
        if system_prompt:
           self.chat_history.append({"role":"assistant","content":system_prompt})
    #添加用户消息到对话历史
    def add_user_message(self,content:str):
        self.chat_history.append({"role":"user","content":content})
    #添加助手消息到对话历史
    def add_assistant_message(self,content:str):
        self.chat_history.append({"role":"assistant","content":content})
    #发送消息并返回助手回复
    def send(self,user_message:str):
        self.add_user_message(user_message)
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.chat_history,
            stream=True,
        )
        full_reply=""
        for chunk in completion:
            if chunk.choices:
                if chunk.choices[0].delta.content:
                    content=chunk.choices[0].delta.content
                    full_reply += content
                    yield content

        self.add_assistant_message(full_reply)



    #获取完整历史
    def get_history(self):
        return self.chat_history
if __name__=="__main__":
    BASE_URL="https://cn-beijing.maas.qianwenaiapi.com/compatible-mode/v1"
    model="qwen3.8-max"
    system_prompt="你是一个 helpful的助手"
    chat = Multiturnchat(base_url=BASE_URL,model=model,system_prompt=system_prompt)
    while True:
        user_input=input("用户输入:")
        if user_input.strip() in ["exit","quit"]:
            break
        if not user_input.strip():
            print("请输入内容")
            continue
        print("助手回复:",end="",flush=True)
        for chunk in chat.send(user_input):
            print(chunk,end="",flush=True)

        print()

