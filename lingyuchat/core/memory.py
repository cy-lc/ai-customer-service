
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage
from langchain_core.messages import BaseMessage
from core.chat_history_manager import ChatHistoryManager
from core.sumarry_manager import SumarryManager
from core.facts_manager import FactsManager
SESSION_KEY="session"
class Memory:
    """记忆管理整合类，组合三个独立管理器"""
    def __init__(self,chat_session_id:str):
        self.chat_session_id=chat_session_id
        self.session_key=f"{SESSION_KEY}:{self.chat_session_id}"
        self.history=ChatHistoryManager(self.session_key)
        self.sumarry=SumarryManager(self.session_key)
        self.facts=FactsManager(self.session_key)


    #========对话历史相关(委托)=========
    def get_session_history(self):
        """获取当前会话的历史记录"""
        return self.history.get_history()
    def get_messages(self):
        """获取当前会话的消息列表"""
        return self.history.get_messages()
    def get_recent_messages(self,recent_n:int):
        """获取最近n条消息列表"""
        return self.history.get_recent_messages(recent_n)
    def get_recent_messages_text(self,recent_n:int):
        """获取最近n条消息的文本内容"""
        messages=self.get_recent_messages(recent_n)
        messages_text=""
        for msg in messages:
            if  isinstance(msg,HumanMessage):
                messages_text+=f"huamn:{msg.content}\n"
            elif isinstance(msg,AIMessage):
                messages_text+=f"ai:{msg.content}\n"
        return messages_text
        for msg in messages:
            if  isinstance(msg,HumanMessage):
                messages_text+=f"huamn:{msg.content}\n"
            elif isinstance(msg,AIMessage):
                messages_text+=f"ai:{msg.content}\n"
        return messages_text
    #===========添加消息(触发摘要逻辑)#===========
    def add_user_messages(self,message:str,llm=None):
        self.history.add_user_message(message)
        self.sumarry.increase_unsumarrized_count()
        #判断是否触发摘要更新
        self._trim_and_summarize(llm)
    def add_ai_messages(self,message:str,llm=None):
        self.history.add_ai_message(message)
        self.sumarry.increase_unsumarrized_count()
        #判断是否触发 摘要更新
        self._trim_and_summarize(llm)

    #=========事实相关=======#
    def get_key_facts(self) -> dict[str,str]:
        """获取当前会话关键事实"""
        return self.facts.get_all_facts()
    def     update_key_facts(self,facts:dict[str,str])->None:
        """更新当前会话的关键事实"""
        self.facts.update_facts(facts)
    def clear_key_facts(self)->None:
        """清空当前会话的关键事实"""
        self.facts.clear_key_facts()


    #==========摘要相关=======#
    def _trim_and_summarize(self,llm=None)->None:
        """截断和摘要"""
        if not self.sumarry.should_trigger_sumarry():#判断是否需要触发摘要
            return
        history=self.history.get_history()#获取当前会话历史记录对象
        if not history:
            return None
        messages=self.get_messages()#获取当前会话消息列表
        unsummarized_count=self.sumarry.get_unsumarrized_count()
        total_count=len(messages)
        sumarrized_count=total_count-unsummarized_count
        #获取未摘要的消息
        new_messages=messages[sumarrized_count:]
        if new_messages:
           old_sumarry=self.sumarry.get_sumarry()#获取旧摘要
           new_sumarry=self.sumarry.generate_incremental_sumarry(
               new_messages,
               old_sumarry,
               llm)#生成新摘要
           self.sumarry.update_sumarry(new_sumarry)#更新摘要
           self.sumarry.reset_unsumarrized_count()#重置未摘要消息计数
           print("已生成新摘要")
    #==========准备llm上下文==========#
    def prepare_llm_context(self,)->list[BaseMessage]:
        """传递给llm的上下文(事实+摘要+最近消息)"""
        result=[]
        #1.添加关键事实
        facts=self.facts.get_all_facts()
        if facts:
            fact_text="|".join([f"{k}:{v}" for k,v in facts.items()])
            result.append(AIMessage(content=f"[关键事实]{fact_text}"))
        #2.添加摘要
        sumarry=self.sumarry.get_sumarry()
        if sumarry:
            result.append(AIMessage(content=f"[摘要]{sumarry}"))
        #3.添加未摘要的消息
        unsummarized_count=self.sumarry.get_unsumarrized_count()
        if unsummarized_count>0:
            messages=self.history.get_messages()#获取所有消息列表
            recent_messages=messages[-unsummarized_count:]
            result.extend(recent_messages)
        return result

























