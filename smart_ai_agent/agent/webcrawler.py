
from langchain_community.document_loaders import WebBaseLoader

def load_document(url:str):
    loader = WebBaseLoader(url)
    docs = loader.load()
    return docs[0]

def load_documents(urls: list[str]):
    loader = WebBaseLoader(urls)
    return loader.load()
