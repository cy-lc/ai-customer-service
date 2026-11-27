from fontTools.misc.arrayTools import vectorLength
from langchain_community.embeddings import DashScopeEmbeddings
embedding_model = DashScopeEmbeddings()
user_input="猫坐在垫子上"
# print(embedding_model.embed_query(user_input))#处理单个文本
user_input2=["猫坐在垫子上","狗坐在垫子上","猫坐在垫子上睡觉"]
results=embedding_model.embed_documents(user_input2)#处理多个文本
for text,vector in zip(user_input2,results):
    print(f"文本:{text}:")
    print(f"向量维度:{len(vector)}:")
    print(vector)
