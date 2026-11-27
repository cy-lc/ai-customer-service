from langchain_community.embeddings import DashScopeEmbeddings

from typing import List, Tuple
from rank_bm25 import BM25Okapi
embedding_model = DashScopeEmbeddings()
import numpy as np
# ========== 余弦相似度函数 ==========
def cosine_similarity(vec1, vec2):
    """余弦相似度（值越大越相似）"""
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

documents = [
    "GPT-4 是OpenAI发布的大语言模型，拥有约1.76万亿个参数",
    "GPT-3 的参数规模为1750亿，参数量比较大，是当时最大的语言模型之一",
    "GPT-3.5 的参数规模为1750亿，相比GPT-3有显著提升",
    "GPT-2 的参数规模为15亿，在当时已经是非常大的模型",
    "大语言模型的参数量直接影响推理能力",
]
# 稠密搜索(相似度搜索)
def vector_search(query:str, docs: list[str])->list[tuple[int, float]]:
    user_query_embedding = embedding_model.embed_query(query)
    document_embeddings = embedding_model.embed_documents(docs)
    similarity = [cosine_similarity(user_query_embedding, doc_vec) for doc_vec in document_embeddings]
    #similarity=[v1,v2,v3,v4,v5]
    #enumerate(similarity)=[(0,v1),(1,v2),(2,v3),(3,v4),(4,v5)]
    ranked=sorted(enumerate(similarity),key=lambda x:x[1],reverse=True)
    return ranked


import jieba
# ========== 4. BM25 关键词搜索 ==========
#稀疏向量(关键字搜索)
def chinese_tokenizer(text: str) -> List[str]:
    """使用 jieba 进行中文分词"""
    return list(jieba.cut(text.strip()))

def bm25_search(query: str, docs: List[str]) -> List[Tuple[int, float]]:
    """BM25检索：返回 (文档索引, BM25分数)"""
    # 使用 jieba 分词
    tokenized_docs = [chinese_tokenizer(doc) for doc in docs]
    bm25 = BM25Okapi(tokenized_docs)
    tokenized_query = chinese_tokenizer(query)
    scores = bm25.get_scores(tokenized_query)
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    return ranked

# RRF融合（Reciprocal Rank Fusion）
def reciprocal_rank_fusion(rank_lists: list[List[Tuple[int, float]]],k:int=60) -> List[Tuple[int, float]]:
    fusion_score={}
    for rank_list in rank_lists:
        for rank, (doc_id, score) in enumerate(rank_list, start=1):
            rrf_score=1/(k+rank)
            if doc_id not in fusion_score:
                fusion_score[doc_id] = 0.0
            fusion_score[doc_id] += rrf_score
    fused=sorted(fusion_score.items(), key=lambda x: x[1], reverse=True)
    return fused



########执行搜索###############
user_query = "GPT-4 参数量"
print("### 稠密搜索结果 ###")
vector_search_results = vector_search(user_query, documents)
for i,score in vector_search_results:
    print(f"文档{i}: {documents[i]}, 相似度: {score}")
bm25_results = bm25_search(user_query, documents)
print("### BM25搜索结果 ###")

for i,score in bm25_results:
    print(f"文档{i}: {documents[i]}, BM25分数: {score}")

print("### RRF融合结果 ###")
rrf_results = reciprocal_rank_fusion([vector_search_results, bm25_results])
for i,score in rrf_results:
    print(f"文档{i}: {documents[i]}, RRF分数: {score}")



