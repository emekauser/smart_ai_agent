from langchain_chroma import Chroma
from langchain.schema import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from dotenv import load_dotenv
import os


# Load environment variables. Assumes that project contains .env file with API keys
load_dotenv()


if not os.getenv("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = "AIzaSyD__T_u-FpDiDiTjJ7SaMy_0kbZpJ99zwg"

CHROMA_PATH = "chroma"
DB_NAME = "smart_ai_documents"
MODEL_NAME = "models/gemini-embedding-exp-03-07"

vector_store = Chroma(
    # collection_name=DB_NAME,
    embedding_function=GoogleGenerativeAIEmbeddings(model=MODEL_NAME))


def add_to_chroma(doc: Document, id: str):
    # Add the document to the vector store
    vector_store.add_documents(documents=[doc], ids=[id])


def add_documents_to_chroma(docs: list[Document], id: list[str]):
    # Add multiple documents to the vector store
    vector_store.add_documents(documents=docs, ids=id)


def update_document_in_chroma(doc: Document, id: str):
    # Update an existing document in the vector store
    vector_store.update_documents(ids=[id], documents=[doc])


def delete_document_from_chroma(id: str):
    # Delete a document from the vector store
    vector_store.delete(ids=[id])


def get_document_from_chroma(id: str) -> Document | None:
    # Retrieve a document from the vector store
    results = vector_store.get_by_ids([id])
    return results[0] if results else None


def search_documents_in_chroma(query: str, k: int = 5) -> list[Document]:
    """
    Search for documents in the vector store based on a query.
    Returns a list of Document objects.
    """
    results = vector_store.similarity_search(query=query)
    return results if results else []


docs = search_documents_in_chroma("accord")
print(f"Search results: {[doc.page_content for doc in docs]}")
