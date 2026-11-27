import os
from pathlib import Path
from log import logger
from indexing_pipeline import IndexingPipeline
from config.setting import QaConfig

PDF_PATH = Path(__file__).parent / "x(1).pdf"


def main():
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        raise RuntimeError("请先设置环境变量 DASHSCOPE_API_KEY")
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"测试用 PDF 不存在: {PDF_PATH}")

    config = QaConfig()
    pipeline = IndexingPipeline(config, api_key)

    file_hash = pipeline.build_from_source(str(PDF_PATH))
    logger.info(f"索引完成，file_hash={file_hash}")

    store = pipeline._vector_store.load_and_build(file_hash)
    logger.info(f"向量库条数: {store._collection.count()}")

    result = store.similarity_search("钟在哪里", k=3)
    for i, doc in enumerate(result, 1):
        logger.info(f"第 {i} 段文本: {doc.page_content[:80]}...")


if __name__=="__main__":
    main()