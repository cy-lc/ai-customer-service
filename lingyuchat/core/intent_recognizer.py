from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
import re
from dataclasses import dataclass
from core.prompt import INTENT_RECOGNIZE_PROMPT
import json
from typing import Any




@dataclass(frozen=True)
class IntentResult:
    intents:list[str]
    slots:dict[str,Any]
    confidence:float
class IntentRecognizer:
    def __init__(self,llm:ChatTongyi):
        self.__prompt=ChatPromptTemplate.from_messages([
            ("system",INTENT_RECOGNIZE_PROMPT),
            ("ai","上下文内容：{chat_history}"),
            ("user","{user_input}")
        ])
        self.__llm=llm
        self.__chain=self.__prompt | self.__llm | StrOutputParser()
    def recognize(self,user_input,chat_history:str=""):
        chat_history=chat_history if chat_history else ""
        result=self.__chain.invoke({"user_input":user_input,"chat_history":chat_history})
        data=self.__parse_str_to_json(result)
        intents=data.get("intents", [])
        if not isinstance(intents, list):
            intent=data.get('intent')
            intents=[intent] if isinstance(intent, str) else []
        slots=data.get("slots") if isinstance(data.get('slots'),dict) else {}
        try:
         confidence=data.get("confidence", 0.0)
        except:
            confidence=0.0
        return IntentResult(intents, slots, confidence)

    def __parse_str_to_json(self, text: str):
                if not text or not text.strip():
                    return {"intents": ["general"], "slots": {}, "confidence": 0.0}
                text = text.strip()
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    pass
                find_text = re.search(r'\{.*?}', text, re.DOTALL)
                if find_text:
                    try:
                        return json.loads(find_text.group())
                    except json.JSONDecodeError:
                        pass



