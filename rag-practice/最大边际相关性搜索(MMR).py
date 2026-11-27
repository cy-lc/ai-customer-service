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
    collection_metadata={"hnsw:space": "cosine"}
)
chroma_db.add_documents(
    documents=data,
    ids=[f"id{i}" for i in range(len(data))]
)
print("普通相似性搜索")
user_query="猫在哪里"
results = chroma_db._similarity_search_with_relevance_scores(user_query, k=3)
print(results)
for i, (result, score) in enumerate(results):
    print(f"第{i+1}个文档: {result.page_content}, 相关性: {score}")

print("最大边际相关性搜索")
mmr_results=chroma_db.max_marginal_relevance_search(
    user_query,
    k=3,
    fetch_k=5,
    lambda_score=0.5
                                                     )
for i, result in enumerate(mmr_results):
    print(f"第{i+1}个文档: {result.page_content}")





