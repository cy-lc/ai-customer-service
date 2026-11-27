from pathlib import Path
from typing import List
from log import logger
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.setting import QaConfig
class PdfIngester:
    """文档加载与切分"""
    SEPARATE=["(?<=。)","(?<=，)","(?<=!)","(?<=？)"," ",""]
    def __init__(self, config: QaConfig):
        self.config = config
        self.splitter=RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            is_separator_regex=True,
            separators=self.SEPARATE
        )
    def  _split_documents(self, documents: List[Document]) -> List[Document]:
       if not documents:
           logger.info("文档为空，无法切分")
           return []
       try:
           chunks=self.splitter.split_documents(documents)
           logger.debug(f"文档切分完成:共{len(documents)}页,共{len(chunks)}块")
           return chunks
       except Exception as e:
           logger.error(f"文档切分失败:{e}")
           return []

    def ingest(self,pdf_source:str) -> List[Document]:
        if not pdf_source:
           raise ValueError("文档源为空")
        if self._is_url(pdf_source):
          logger.info(f"检测到文档源为URL，开始加载文档：{pdf_source}")
          return self._ingest_from_url(pdf_source)
        else:
          logger.info(f"检测到文档源为本地文件")
          return self._ingest_from_local_file(pdf_source)


    def _is_url(self, source: str) -> bool:
        try:
            return source.startswith("http://") or source.startswith("https://")
        except Exception as e:
            return False
    def _ingest_from_url(self, url: str) -> List[Document]:
        """从URL加载文档"""
        try:
            loader = PyPDFLoader(url)
            documents = loader.load()
            return self._split_documents(documents)
        except Exception as e:
            raise ValueError(f"从本地文件加载文档失败:{e}")
    def _ingest_from_local_file(self, file_path: str) -> List[Document]:
        """从本地文件加载文档"""
        path=Path(file_path)
        if not path.exists():
          raise  ValueError(f"文件不存在:{file_path}")
        if not path.is_file():
          raise  ValueError(f"路径不是文件:{file_path}")
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            return self._split_documents(documents)
        except Exception as e:
            raise ValueError(f"从本地文件加载文档失败:{e}")


if __name__ == "__main__":
    pdf_path = "C:\\Users\\30133\\PycharmProjects\\WelcomeScreen\\study\\smart_reading\\x.pdf"
    ingester = PdfIngester(QaConfig())
    data= ingester.ingest(pdf_path)
    print(data)
    print(len(data))


