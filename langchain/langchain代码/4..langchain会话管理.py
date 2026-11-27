# ========== 会话存储管理类 ==========
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from typing import Dict, List
_session_store: Dict[str, BaseChatMessageHistory] = {}

class Memory:
    def get_session_history(self, chat_session_id: str) -> BaseChatMessageHistory:
        if chat_session_id not in _session_store:
            _session_store[chat_session_id] = InMemoryChatMessageHistory()
        return _session_store[chat_session_id]

    def add_human_message(self, chat_session_id: str, message: str | HumanMessage) -> None:
        chat_history = self.get_session_history(chat_session_id)
        if isinstance(message, str):
            chat_history.add_message(HumanMessage(content=message))
        else:
            chat_history.add_message(message)

    def add_ai_message(self, chat_session_id: str, message: str | AIMessage) -> None:
        chat_history = self.get_session_history(chat_session_id)
        if isinstance(message, str):
            chat_history.add_message(AIMessage(content=message))
        else:
            chat_history.add_message(message)

    def messages(self, chat_session_id: str) -> List[BaseMessage]:
        return self.get_session_history(chat_session_id).messages

    # ========== 对话类 ==========
class ChatSession:
    def __init__(self, session_id: str, system_prompt: str = "你是一个友好的AI助手。"):
            self.session_id = session_id
            self.memory = Memory()
            self.model = ChatTongyi(model="qwen-max", streaming=True)
            self.prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}")
            ])
            self.parser = StrOutputParser()

            self.chain = self.prompt | self.model | self.parser

    def send(self, user_input: str):
            chat_history = self.memory.messages(self.session_id)

            stream = self.chain.stream({
                "chat_history": chat_history,
                "input": user_input
            })

            full_reply = ""
            for chunk in stream:
                full_reply += chunk
                yield chunk

            self.memory.add_human_message(self.session_id, user_input)
            self.memory.add_ai_message(self.session_id, full_reply)
if __name__=="__main__":
    session=ChatSession("110")
    print("用户：你好")
    print("AI：", end="")
    for chunk in session.send("你好"):
        print(chunk, end="", flush=True)


    print("用户：刚刚我说了什么")
    print("AI：", end="")
    for chunk in session.send("刚刚我说了什么"):
        print(chunk, end="", flush=True)

