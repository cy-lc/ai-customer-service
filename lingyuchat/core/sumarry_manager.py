from typing import List, Dict
from langchain_core.messages import HumanMessage,AIMessage

from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from core.sumarry_prompt import SUMMARY_GENERATION_PROMPT
from langchain_core.messages import BaseMessage

from requests import session
#未知摘要key是chat_session_id,value是摘要内容
_sumarry_store:Dict[str,str]={}
#未摘要的key是chat_session_id,value是未摘要的聊天内容
_unsumarrized_conut:Dict[str,int]={}
#默认配置
SUMARRY_BATCH_SIZE=12


class SumarryManager:
    def __init__(self,session_id:str,llm:ChatTongyi|None=None):
        self.session_id=session_id
        if session_id not in _sumarry_store:
            _sumarry_store[session_id]=""
        if session_id not in _unsumarrized_conut:
            _unsumarrized_conut[session_id]=0

    def get_sumarry(self)->str:
        """获取摘要"""
        return _sumarry_store.get(self.session_id,"")
    def update_sumarry(self,new_sumarry:str):
        """更新摘要"""
        _sumarry_store[self.session_id]=new_sumarry
    def get_unsumarrized_count(self)->int:
        """获取未摘要消息数量"""
        return _unsumarrized_conut.get(self.session_id,0)
    def increase_unsumarrized_count(self,amount:int=1):
        """增加未摘要消息数量"""
        current=_unsumarrized_conut.get(self.session_id,0)
        _unsumarrized_conut[self.session_id]=current+amount
    def reset_unsumarrized_count(self):
        """重置未摘要消息数量"""
        _unsumarrized_conut[self.session_id]=0
    def should_trigger_sumarry(self)-> bool:
        """是否触发摘要"""
        return self.get_unsumarrized_count()>=SUMARRY_BATCH_SIZE


    """生成增量摘要"""
    def generate_incremental_sumarry(
            self,old_sumarry:str,
            new_messages:List[BaseMessage],
            llm:ChatTongyi|None=None
    )->str:
        if not new_messages:
            return old_sumarry
        #提取消息新文本
        messages_text=""
        for msg in new_messages:
           if isinstance(msg,HumanMessage):
               messages_text+=f"human:{msg.content}\n"
           elif isinstance(msg,AIMessage):
               messages_text+=f"ai:{msg.content}\n"
        if not llm:
            return self.simple_summary(old_sumarry,messages_text)
        try:
            sumarry_prompt=ChatPromptTemplate.from_messages([
                ("system",SUMMARY_GENERATION_PROMPT),
                ("human",f"旧摘要:{old_sumarry}\n新消息:{messages_text}")
            ])
            chain=sumarry_prompt|llm|StrOutputParser()
            result=chain.invoke(input={})
            new_sumarry=result.strip()
            return new_sumarry
        except Exception:
            return self.simple_summary(old_sumarry,messages_text)
    def simple_summary(self,old_sumarry:str,messages_text:str)->str:
        if old_sumarry and old_sumarry!=['摘要:无']:
          old_part=old_sumarry[0:150] if len(old_sumarry)>150 else old_sumarry
          new_part=messages_text[0:150] if len(messages_text)>150 else messages_text
          return f"[摘要: {old_part} {new_part}]"
        else:
           new_part = messages_text[0:150] if len(messages_text) > 150 else messages_text
           return f"[摘要: {messages_text}]"






