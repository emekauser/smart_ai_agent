import asyncio
from langchain_postgres.vectorstores import PGVector
from langchain.schema import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from google.ai.generativelanguage_v1beta import (
    GenerativeServiceAsyncClient as v1betaGenerativeServiceAsyncClient,
)

from dotenv import load_dotenv
import os

load_dotenv()
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")


if not db_name or not db_user or not db_password or not db_host:
    raise ValueError(
        "Database connection details are not set in the environment variables.")

COLLECTION = "smart_ai_documents_1"
MODEL_NAME = "models/gemini-embedding-exp-03-07"
CONNECTION = f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:5432/{db_name}"
CONNECTION = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:5432/{db_name}"

vector_store = PGVector(
    embeddings=GoogleGenerativeAIEmbeddings(model=MODEL_NAME),
    collection_name=COLLECTION,
    connection=CONNECTION,
    use_jsonb=True,
    async_mode=True,
)


def add_document_to_vector_store(doc: Document, id: str):
    # Add the document to the vector store
    print(f"document: {doc}, id: {id}")
    vector_store.add_documents(documents=[doc], ids=[id])


def add_documents_to_vector_store(docs: list[Document], id: list[str]):
    # Add multiple documents to the vector store
    vector_store.add_documents(documents=docs, ids=id)


def update_document_to_vector_store(doc: Document, id: str):
    # Update an existing document in the vector store
    vector_store.update_documents(ids=[id], documents=[doc])


def delete_document_from_vector_store(id: str):
    # Delete a document from the vector store
    vector_store.delete(ids=[id])


def get_document_from_vector_store(id: str) -> Document | None:
    # Retrieve a document from the vector store
    results = vector_store.get_by_ids([id])
    return results[0] if results else None


def search_documents_in_vector_store(query: str, k: int = 5) -> list[Document]:
    """
    Search for documents in the vector store based on a query.
    Returns a list of Document objects.
    """
    results = vector_store.similarity_search(query=query)
    print(f"Search results: {results}")
    return results if results else []


class VectorStoreInterface:
    vector_store: PGVector = None

    def __init__(self):
        self.init_vectorstore()

    def init_vectorstore(self):
        self.vector_store = PGVector(
            embeddings=GoogleGenerativeAIEmbeddings(model=MODEL_NAME),
            collection_name=COLLECTION,
            connection=CONNECTION,
            use_jsonb=True,
            async_mode=True,
        )

    async def add_document(self, doc: Document, id: str):
        # Add the document to the vector store
        print(f"document: {doc}, id: {id}")
        await self.vector_store.aadd_documents(documents=[doc], ids=[id])

    async def add_documents(self, docs: list[Document], ids: list[str]):
        # Add multiple documents to the vector store
        await self.vector_store.aadd_documents(documents=docs, ids=ids)

    async def update_document(self, doc: Document, id: str):
        # Update an existing document in the vector store
        await self.vector_store.aupdate_documents(ids=[id], documents=[doc])

    async def delete_document(self, id: str):
        # Delete a document from the vector store
        await self.vector_store.adelete(ids=[id])

    async def get_document(self, id: str) -> Document | None:
        # Retrieve a document from the vector store
        results = await self.vector_store.aget_by_ids([id])
        return results[0] if results else None

    async def search_documents(self, query: str, k: int = 5) -> list[Document]:
        """
        Search for documents in the vector store based on a query.
        Returns a list of Document objects.
        """
        results = await self.vector_store.asimilarity_search(query=query)
        return results if results else []


async def test():
    em = GoogleGenerativeAIEmbeddings(model=MODEL_NAME)
    res = await em.aembed_documents(texts=["The weather is sunny and cold."])
    await vector_store.aadd_embeddings(
        texts=["The weather is sunny and cold."], embeddings=res)
    print(res)

# vector_store = VectorStoreInterface()

# print(search_documents_in_vector_store("how to book a flight"))
# asyncio.run(test())
# asyncio.run(
#     vector_store.add_documents(
#         [
#             Document(page_content="The weather is sunny and warm."),
#             Document(page_content="I want to book a flight to New York."),
#         ],
#         ["doc3", "doc4"]
#     ))
