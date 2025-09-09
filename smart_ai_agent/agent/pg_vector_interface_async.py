import os
import asyncpg

from langchain_postgres.utils.pgvector_migrator import alist_pgvector_collection_names, amigrate_pgvector_collection
from langchain_postgres import PGEngine, PGVectorStore, Column
from langchain.schema import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv


load_dotenv()
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")


if not db_name or not db_user or not db_password or not db_host:
    raise ValueError(
        "Database connection details are not set in the environment variables.")

VECTOR_SIZE = 3072
COLLECTION = "smart_ai_documents"
MODEL_NAME = "models/gemini-embedding-exp-03-07"
CONNECTION = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:5432/{db_name}"

embedding = GoogleGenerativeAIEmbeddings(model=MODEL_NAME)
engine = PGEngine.from_connection_string(url=CONNECTION)


class VectorStoreInterface:
    vector_store: PGVectorStore = None
    embedding: GoogleGenerativeAIEmbeddings = None

    def __init__(self):
        self.embedding = GoogleGenerativeAIEmbeddings(model=MODEL_NAME)

    @classmethod
    async def connect(cls):
        my_instance = cls()
        await my_instance.create_table_if_not_exist()
        await my_instance.init_vectorstore()
        return my_instance

    async def is_table_exist(self):
        conn = await asyncpg.connect(CONNECTION.replace("+asyncpg", ""))
        exists = False
        try:
            query = """
                SELECT EXISTS (
                    SELECT FROM
                        pg_tables
                    WHERE
                        schemaname = $1 AND tablename = $2
                );
            """
            exists = await conn.fetchval(query, "public", COLLECTION)
        finally:
            await conn.close()
        return exists

    async def create_table_if_not_exist(self):
        if not self.vector_store and not await self.is_table_exist():
            await engine.ainit_vectorstore_table(
                table_name=COLLECTION,
                vector_size=VECTOR_SIZE,
                id_column=Column("langchain_id", "VARCHAR")
            )

    async def init_vectorstore(self):
        self.vector_store = await PGVectorStore.create(
            engine=engine,
            table_name=COLLECTION,
            embedding_service=self.embedding
        )

    async def add_document(self, doc: Document, id: str):
        # Add the document to the vector store
        await self.add_documents(docs=[doc], ids=[id])

    async def add_documents(self, docs: list[Document], ids: list[str]):
        # Add multiple documents to the vector store
        texts = [doc.page_content for doc in docs]
        embeddings = await self.embedding.aembed_documents(texts=texts)
        await self.vector_store.aadd_embeddings(texts=texts, embeddings=embeddings, ids=ids)

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
        embed_query = await self.embedding.aembed_documents(texts=[query])
        results = await self.vector_store.asimilarity_search_by_vector(embedding=embed_query[0])
        return results if results else []


class VectorStoreMigration:
    engine: PGEngine
    all_collection_names = None

    def __init__(self):
        self.engine = PGEngine.from_connection_string(url=CONNECTION)

    async def get_all_collections(self):
        self.all_collection_names = await alist_pgvector_collection_names(self.engine)

    async def migrate_documents(self):
        for collection_name in self.all_collection_names:
            destination_vector_store = await PGVectorStore.create(
                self.engine,
                embedding_service=embedding,
                table_name=collection_name,
            )

            await amigrate_pgvector_collection(
                engine,
                collection_name=collection_name,
                vector_store=destination_vector_store,
                delete_pg_collection=False,
            )

    async def create_vectorstore_tables(self):
        for collection_name in self.all_collection_names:
            await self.engine.ainit_vectorstore_table(
                table_name=collection_name,
                vector_size=3072,
                id_column=Column("langchain_id", "VARCHAR")
            )

    async def migrate(self):
        await self.get_all_collections()
        await self.create_vectorstore_tables()
        await self.migrate_documents()
