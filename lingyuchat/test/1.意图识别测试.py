from langchain_community.chat_models import ChatTongyi
from core.intent_recognizer import IntentRecognizer
if __name__ == "__main__":
    llm = ChatTongyi(model="qwen-flash")
    intent_recognizer = IntentRecognizer(llm)
    result = intent_recognizer.recognize("你好,ai")

    print(result)