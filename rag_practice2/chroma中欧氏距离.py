from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings import DashScopeEmbeddings
import numpy as np

embedding_model = DashScopeEmbeddings()

texts = [
    "小猫喜欢在软垫上睡觉。",
    "猫坐在垫子上。",
    "猫咪经常趴在垫子上休息。",
    "一只猫正在垫子上打盹。",
    "小狗喜欢在院子里玩飞盘。",
    "金毛犬在草地上奔跑。",
    "金鱼在水缸里游来游去。",
    "今天天气很好，适合出去散步。",
    "这只小奶猫白天大部分时间都在垫子上睡觉。"
]
data = [Document(page_content=doc) for doc in texts]
chroma_db = Chroma(
    collection_name="my_collection",
    embedding_function=embedding_model,
    persist_directory="./chroma_db",
    collection_metadata={"hnsw:space": "l2"},#不写也是默认欧氏距离


)
chroma_db.add_documents(
    documents=data,
    ids=[f"id{i}" for i in range(len(data))]
)
print("普通相似性搜索")
user_query="猫在哪里"
results = chroma_db.similarity_search(user_query, k=3)#不显示欧氏距离
results2 = chroma_db.similarity_search_with_score(user_query, k=3)#显示欧氏距离
print(results)
print(results2)

