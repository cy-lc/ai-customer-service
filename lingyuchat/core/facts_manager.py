from typing import List, Dict
# 全局存储：关键事实（key是chat_session_id, value是插槽slots）
_fact_store:Dict[str,Dict[str,str]]={}
class FactsManager:
    def __init__(self,chat_session_id:str):
        self.chat_session_id=chat_session_id
        if chat_session_id not in _fact_store:
            _fact_store[chat_session_id]={}

    def get_all_facts(self)->Dict[str,str]:
        """获取当前所有事实"""
        return _fact_store.get(self.chat_session_id,{}).copy()
    def get_fact(self,key:str):
        """获取某个事实"""
        return _fact_store.get(self.chat_session_id,{}).get(key,"")
    def update_facts(self,facts:Dict[str,str])->None:
        """更新事实"""
        if self.chat_session_id not in _fact_store:
              _fact_store[self.chat_session_id]={}
        _fact_store[self.chat_session_id].update({
               k:v for k,v in facts.items() if v
           })
    def set_fact(self,key:str,value:str)->None:
        """设置某个事实"""
        if self.chat_session_id not in _fact_store:
            _fact_store[self.chat_session_id]={}
        if value:
            _fact_store[self.chat_session_id][key]=value
    def clear_key_facts(self)->None:
        """清空当前会话所有事实"""
        if self.chat_session_id in _fact_store:
            _fact_store[self.chat_session_id]={}
    def delete_session(self)->None:
        """删除当前会话所有事实"""
        if self.chat_session_id in _fact_store:
            del _fact_store[self.chat_session_id]







