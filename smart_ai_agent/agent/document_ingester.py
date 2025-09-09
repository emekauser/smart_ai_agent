from langchain_community.document_loaders import DirectoryLoader
from langchain.schema import Document

from .pg_vector_interface import add_documents_to_vector_store


async def load_documents_from_directory(directory: str) -> list[Document]:
    """
    Load all documents from a specified directory.
    """
    loader = DirectoryLoader(directory,  glob="*.md")
    docs = await loader.aload()

    return docs


async def add_documents_from_directory(directory: str):
    """
    Load documents from a directory and add them to the vector store.
    """
    docs = await load_documents_from_directory(directory)
    ids = [f"document_{i}" for i in range(len(docs))]
    add_documents_to_vector_store(docs, ids)

    print(f"Added {len(docs)} documents from {directory} to the vector store.")
