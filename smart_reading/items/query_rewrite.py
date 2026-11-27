
from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from typing import List, Optional
from query_prompt import REWRITE_PROMPT
from log  import logger



class QueryRewriter:
    # 需要改写的关键词（存在这些词时触发改写）
    REFERENCE_KEYWORDS = ["那篇", "刚才", "它", "这个", "该", "那", "这", "其"]

    def __init__(self, llm: ChatTongyi) -> None:
        """
        初始化查询改写器
        :param llm: 大语言模型实例
        """
        self._llm = llm
        self._prompt = ChatPromptTemplate.from_messages([
            ("system", REWRITE_PROMPT),
            MessagesPlaceholder("chat_history"),
            ("human", "用户问题：{question}\n改写后的查询：")
        ])
        self._chain = self._prompt | llm | StrOutputParser()

    def rewrite(self,
                question: str,
                chat_history:Optional[List[BaseMessage]]=None) -> str:
        """
        改写查询
        :param question: 用户原始问题
        :param chat_history: 对话历史
        :return: 改写后的查询
        """
        # 1. 参数校验
        question = (question or "").strip()
        if not question:
            logger.warning("问题无需改写")
            return question

        # 2. 判断是否需要改写（短问题或无指代词的问题跳过）
        if not self._needs_rewrite(question):
            return question
        # 3. 调用大语言模型进行改写
        try:
            chat_history = chat_history or []
            rewrite=self._chain.invoke({
                "question": question,
                "chat_history": chat_history
            })
            return rewrite
        except:
            logger.warning("改写失败，返回原始问题")
            return question


    def _needs_rewrite(self, question: str) -> bool:
        """
        判断问题是否需要改写
        :param question: 问题字符串
        :return: 是否需要改写
        """
        # 问题太短（少于5个字）或包含代词
        if len(question) < 5:
            return False
        return any(keyword in question for keyword in self.REFERENCE_KEYWORDS)



if __name__ == "__main__":
    query_rewriter = QueryRewriter(llm=ChatTongyi(model="qwen-max"))
    print(query_rewriter.rewrite("", [AIMessage(content="")]))
