
from urllib.parse import urlparse
from langchain_community.embeddings import DashScopeEmbeddings
from config.setting import QaConfig
from vector_storage import VectorStoreManager
from hash_calculate import HashCalculate
from ingest import  PdfIngester
import requests
from log import logger



class IndexingPipeline:
    def __init__(self, config: QaConfig,dashscope_api_key):
        self.config = config
        self._hash_calculator = HashCalculate()
        self._ingestor = PdfIngester(config)
        self._vector_store = VectorStoreManager(self.config, DashScopeEmbeddings(
            model=self.config.embedding_model,
            dashscope_api_key=dashscope_api_key
        ))


    def build_from_source(self, pdf_source: str):
        if not pdf_source:
            raise ValueError("PDF源不能为空")

        # 1. 计算文件哈希
        file_hash = self._compute_hash(pdf_source)
        logger.info(f"pdf文件哈希: {file_hash}")
        #2.加载并切割文档
        chunks=self._ingestor.ingest(pdf_source)
        if not chunks:
            raise ValueError("PDF切分后未生成文本块")
        #3.构建向量数据库
        self._vector_store.load_and_build(file_hash,chunks)
        logger.info("向量数据库构建完成")
        return file_hash


    def _compute_hash(self,pdf_source:str):
        # 判断是否为URL
        try:
            result = urlparse(pdf_source)
            is_url = all([result.scheme in ['http', 'https'], result.netloc])
        except Exception:
            is_url = False

        if is_url:
            # URL: 下载后计算哈希
            response = requests.get(pdf_source, timeout=30)
            response.raise_for_status()
            pdf_bytes = response.content
            return self._hash_calculator.compute_hash(pdf_bytes)
        else:
            # 本地文件: 流式计算哈希
            return self._hash_calculator.compute_hash_from_file(pdf_source)



