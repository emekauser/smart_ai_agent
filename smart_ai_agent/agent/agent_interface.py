from .pg_vector_interface import add_document_to_vector_store, add_documents_to_vector_store, update_document_to_vector_store, delete_document_from_vector_store, get_document_from_vector_store, search_documents_in_vector_store
from .pg_vector_interface_async import VectorStoreInterface
from .webcrawler import load_document, load_documents
from api.models import Document


def add_document(url: str):
    """
    Add a document to the vector store and database.
    """
    doc = load_document(url)
    document = Document.objects.create(
        title=doc.metadata.get('title', 'Untitled'),
        file_type=doc.metadata.get('file_type', 'html'),
        content=doc.page_content,
        url=url
    )
    add_document_to_vector_store(doc, str(document.id))


def add_documents(urls: list[str]):
    """
    Add multiple documents to the vector store and database.
    """
    docs = load_documents(urls)
    documents = [Document(
        title=doc.metadata.get('title', 'Untitled'),
        file_type=doc.metadata.get('file_type', 'html'),
        content=doc.page_content,
        url=urls[urls.index(doc.metadata.get('source', urls[i]))]
    ) for i, doc in enumerate(docs)]

    documents = Document.objects.bulk_create(documents)

    ids = [str(doc.id) for doc in documents]
    add_documents_to_vector_store(docs, ids)


async def load_documents(docs) -> list[Document]:
    """
    Load all documents from a specified directory and add them to the vector store.
    """
    vector_store_interface = await VectorStoreInterface.connect()

    documents = [Document(
        title=doc.metadata.get('title', 'Untitled'),
        file_type="md",
        content=doc.page_content,
    ) for doc in docs]
    documents = await Document.objects.abulk_create(documents)

    ids = [str(doc.id) for doc in documents]
    await vector_store_interface.add_documents(docs, ids)


def update_document(document: Document):
    """
    Update an existing document in the vector store and database.
    """
    doc = load_document(document.url)
    document.title = doc.metadata.get('title', 'Untitled')
    document.content = doc.page_content
    document.save()

    update_document_to_vector_store(doc, str(document.id))


def re_index_document(document: Document):
    """
    Update an existing document in the vector store and database.
    """
    doc = load_document(document.url)
    document.title = doc.metadata.get('title', 'Untitled')
    document.content = doc.page_content
    document.save()

    vector_doc = get_document_from_vector_store(str(document.id))
    if not vector_doc:
        add_document_to_vector_store(doc, str(document.id))
    else:
        update_document_to_vector_store(doc, str(document.id))


def delete_document(document: Document):
    """
    Delete a document from the vector store and database.
    """

    delete_document_from_vector_store(str(document.id))
    document.delete()


def get_document_from_vector_db(id: int) -> Document | None:
    """
    Retrieve a document from the vector store.
    """
    return get_document_from_vector_store(str(id))


def search_documents(query: str) -> list[Document]:
    """
    Search for documents in the vector store based on a query.
    Returns a list of Document objects.
    """
    return search_documents_in_vector_store(query, k=5)
