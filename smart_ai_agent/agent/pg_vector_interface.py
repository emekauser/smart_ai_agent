from langchain_postgres.vectorstores import PGVector
from langchain.schema import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from dotenv import load_dotenv
import os

load_dotenv()
if not os.getenv("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = "AIzaSyD__T_u-FpDiDiTjJ7SaMy_0kbZpJ99zwg"
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")


if not db_name or not db_user or not db_password or not db_host:
    raise ValueError(
        "Database connection details are not set in the environment variables.")

COLLECTION = "smart_ai_documents"
MODEL_NAME = "models/gemini-embedding-exp-03-07"
CONNECTION = f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:5432/{db_name}"

vector_store = PGVector(
    embeddings=GoogleGenerativeAIEmbeddings(model=MODEL_NAME),
    collection_name=COLLECTION,
    connection=CONNECTION,
    use_jsonb=True,
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
    return results if results else []
