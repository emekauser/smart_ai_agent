
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework import status
from adrf.decorators import api_view
from rest_framework import status

from .models import Document
from .serializer import DocumentSerializer
from agent.agent_interface import add_document, add_documents, update_document, delete_document, re_index_document, get_document_from_vector_db, search_documents
from agent.agent import invoke_agent


@api_view(['GET', 'POST'])
def document_list(request):
    if request.method == 'GET':
        documents = Document.objects.all()
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        urls = request.data.get('urls', '')
        if("," in urls):
            urls = urls.split(",")
            add_documents(urls)
        else:
            add_document(urls)
        return Response({"message": "Documents added successfully"}, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def document_detail(request, pk):
    try:
        document = Document.objects.get(pk=pk)
    except Document.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DocumentSerializer(document)
        return Response(serializer.data)

    elif request.method == 'PUT':
        url = request.data.get('url')
        if url:
            document.url = url
            update_document(document)
            serializer = DocumentSerializer(document)
            return Response({"message": "Document updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        delete_document(document)
        return Response({"message": "Document deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view([ 'PUT'])
def re_index_document_to_vector_db(request, pk):
    try:
        document = Document.objects.get(pk=pk)
    except Document.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    re_index_document(document)
    serializer = DocumentSerializer(document)
    return Response({"message": "Document updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

@api_view([ 'GET'])
def get_document_in_vector_db(request, pk):
    try:
        document = Document.objects.get(pk=pk)
    except Document.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
  
    vector_doc = get_document_from_vector_db(str(document.id))
    if not vector_doc:
        return Response({"message": "Document not found in vector database"}, status=status.HTTP_404_NOT_FOUND)
    
    print(vector_doc)
    data = {
        "title": vector_doc.metadata.get('title', 'Untitled'),
        "content": vector_doc.page_content
    }
    return Response({"message": "Document found in vector database", "data": data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def ask_agent(request):
    query = request.data.get('query', '')

    response = invoke_agent(query)
    print(response)
    return Response({"response": response}, status=status.HTTP_200_OK)
