import asyncio
from langchain_community.document_loaders import DirectoryLoader
from langchain.schema import Document

from agent.agent_interface import load_documents


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
    print("Loading documents...")
    docs = await load_documents_from_directory(directory)

    print("Adding documents to vector store...")
    await load_documents(docs)

    print(
        f"Added {len(docs)} documents from {directory} to the vector store.")


asyncio.run(add_documents_from_directory("data"))
