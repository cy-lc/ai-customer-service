


from run import PDFQA
import os
import  sys
pdf_path = "C:\\Users\\30133\\PycharmProjects\\WelcomeScreen\\study\\smart_reading\\x(1).pdf"

api_key = os.environ.get("DASHSCOPE_API_KEY")
qa = PDFQA(pdf_path, api_key=api_key)

# 模拟逐条发送
q1 = "钟究竟在哪里"
r1 = qa.ask(q1)
print(f"Q: {q1}\nA: {r1['answer']}\n")

q2 = "他为什么不修钟"  # 这里的“它”依赖上一轮历史
r2 = qa.ask(q2)
print(f"Q: {q2}\nA: {r2['answer']}\n")
