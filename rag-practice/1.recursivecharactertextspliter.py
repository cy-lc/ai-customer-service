from langchain_community.document_loaders import TextLoader
from langchain_core import documents
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

file_path="C:\\Users\\30133\\PycharmProjects\\WelcomeScreen\\study\\rag-practice\\历史文化.text"
loader=TextLoader(file_path=file_path, encoding='utf-8')
docs=loader.load()
print(docs)
print(type(docs))
print(len(docs))
print(docs[0].page_content)
print(docs[0].metadata)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=10,
    separators=["。", "！", "?"],
    chunk_overlap=0,
    length_function=len,
)
chunks=text_splitter.split_text(docs[0].page_content)
for i,chunk in enumerate(chunks):
    print(f"Chunk {i+1}:")
    print(chunk)


# RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=10,
    separators=[r"(?<=。)", r"(?<=！)", r"(?<=\?)"],
    chunk_overlap=0,
    is_separator_regex=True,
    length_function=len,
)
chunks=text_splitter.split_text(docs[0].page_content)
for i,chunk in enumerate(chunks):
    print(f"Chunk {i+1}:")
    print(chunk)






