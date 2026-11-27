#普通提示词
# from langchain_community.llms.tongyi import Tongyi
# llm = Tongyi(model="qwen-max")
# user_query="你是一个{expert}专家，请你解释一下{content}".format(expert="AI",content="什么是AI")
# ai_response = llm.invoke(user_query)
# print(ai_response)
from typing import Protocol

# #prompt_template 模板提示词
# from langchain_community.llms.tongyi import Tongyi
# from langchain_core.prompts import PromptTemplate
# llm = Tongyi(model="qwen-max")
# prompt_template=PromptTemplate.from_template(
#     "你是一个{expert}专家，请你解释一下{content}"
# )
# prompt=prompt_template.format(expert="ai",content="什么是rag")
# result= llm.stream(prompt)
# for chunk in result:
#     print(chunk,end="", flush=True)


#prompt_template + llm
# from langchain_community.llms.tongyi import Tongyi
# from langchain_core.prompts import PromptTemplate
# prompt_template=PromptTemplate.from_template(
#     "你是一个{expert}专家，请你解释一下{content}"
# )
# llm = Tongyi(model="qwen-max")
# chain=prompt_template | llm
# result= chain.stream({"expert":"ai","content":"什么是rag"})
# for chunk in result:
#     print(chunk,end="", flush=True)

#
# #FewShotPromptTemplate+llm
# from langchain_community.llms.tongyi import Tongyi
# from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
# examples=[
#     {"input":"开心","output":"高兴"},
#     {"input":"快速","output":"迅猛"},
#     {"input":"美丽","output":"绚丽"}
# ]
# prompt_example=PromptTemplate.from_template(
#     template="输入：{input}\n输出：{output}"
# )
# few_shot_prompt_template=FewShotPromptTemplate(
#     examples=examples,
#     example_prompt=prompt_example,
#     prefix="根据输入给出对应的输出",
#     suffix="基于实例回答问题。用户输入：{word}\n输出：",
#     input_variables=["word"]
# )
# # prompt_text=few_shot_prompt_template.format(word="开心")
# # print(prompt_text)
# llm = Tongyi(model="qwen-max")
# chain=few_shot_prompt_template | llm
# result=chain.stream({"word":"飞翔"})
# for chunk in result:
#     print(chunk,end="", flush=True)



#ChatPromptTemplate+llm
from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
chat_prompt_template=ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个ai"),
        MessagesPlaceholder("history"),
        ("human", "我刚刚问了什么"),
    ]
)
chat_history=[
    ("human", "1+1等于多少"),
    ("ai", "等于3")

]
# llm=Tongyi(model="qwen-max")
# chain=chat_prompt_template | llm
# result=chain.invoke({"history":chat_history})
# print(result)

result=chat_prompt_template.invoke(input={"history":chat_history}).to_string()
llm=Tongyi(model="qwen-max")

print(llm.invoke(result))
print(type(result))


# print(result)
# llm = Tongyi(model="qwen-max")
# chain=chat_prompt_template | llm
# result=chain.stream({"expert":"ai","content":"rag"})
# for chunk in result:
#     print(chunk,end="", flush=True)




