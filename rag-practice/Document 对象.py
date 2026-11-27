
from langchain_core.documents import Document


# 创建单个 Document 对象
doc = Document(
    page_content="这是一段测试的文本内容。",
    metadata={
        "source": "test.txt",
        "author": "张三",
        "page": 1
    }
)

# 打印看看
print(doc.page_content)
print(doc.metadata)



