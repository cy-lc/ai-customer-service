
from log import logger
from pathlib import Path
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma
from config.setting import QaConfig
from langchain_core.documents import Document
from typing import Optional, List


class VectorStoreManager:
    def __init__(self, config: QaConfig, embeddings:DashScopeEmbeddings):
        self.config = config
        self.embeddings = embeddings


    def load_and_build(self,
                       file_hash: str,
                       chunks: Optional[List[Document]] = None)->Chroma:
        """
        :param file_hash: 哈希值
        :param chunks: 切分后的文档列表
        :return: Chroma 向量库实例
        """
        if not file_hash:
            raise ValueError("文件哈希不能为空")
        persist_directory=self._get_persist_directory(file_hash)
        collection_name=self._get_collection_name(file_hash)
        vector_store = Chroma(persist_directory=str(persist_directory),#路径
                              collection_name=collection_name,
                              embedding_function=self.embeddings,
                              # Deleted:collection_metadata={"hnsw_space": "cosine"},
                              collection_metadata={"hnsw:space": "cosine"},
                              )
        if self._has_data(vector_store):
            logger.info("向量库中已存在数据，将使用现有数据")
            return vector_store
        if not chunks:
            raise ValueError("文档切分结果不能为空")
        logger.info("向量库中不存在数据，将创建新数据")
        return self._build_vector_store(vector_store, chunks)



    def _build_vector_store(self,
                           vector_store: Chroma,
                           chunks:List[Document]
       ) -> Chroma:
        if not chunks:
            raise ValueError("文档切分结果不能为空")
        try:
            vector_store.add_documents(
                documents=chunks,
                ids=[f"doc_{idx}" for idx in range(1,len(chunks)+1)]
            )
            logger.info("向量库构建完成")
            return vector_store
        except Exception as e:
            logger.error(f"向量库构建出错: {e}")
            raise e


        """构建向量库"""
    def _get_persist_directory(self,file_hash)->Path:
        persist_directory = Path(self.config.chroma_root_dir) /f"{file_hash}"
        persist_directory.mkdir(parents=True, exist_ok=True)
        return persist_directory

    def _get_collection_name(self,file_hash)->str:
      collection_name = f"{self.config.collection_prefix}_{file_hash}"
      return collection_name

    def _has_data(self,vector_store: Chroma) -> bool:
     """判断向量库中是否存在数据"""
     try:
         return vector_store._collection.count() > 0
     except Exception as e:
        logger.warning(f"判断向量库中是否存在数据时出错:{e}")
        return False


