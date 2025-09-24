
import uuid

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes


from .models import Document, UserChatSession
from .serializer import DocumentSerializer
from agent.agent_interface import add_document, add_documents, update_document, delete_document, re_index_document, get_document_from_vector_db
from agent.agents.flight_manager_agent import ask_for_help
from .chat_session import ChatSession


@api_view(['GET', 'POST'])
def document_list(request):
    if request.method == 'GET':
        documents = Document.objects.all()
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        urls = request.data.get('urls', '')
        if ("," in urls):
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


@api_view(['PUT'])
def re_index_document_to_vector_db(request, pk):
    try:
        document = Document.objects.get(pk=pk)
    except Document.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    re_index_document(document)
    serializer = DocumentSerializer(document)
    return Response({"message": "Document updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_document_in_vector_db(request, pk):
    print(request.user)
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


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def ask_agent(request):
    query = request.data.get('query', '')
    user = request.user

    chat_session = ChatSession(user)
    user_session = chat_session.get_current_session()

    if user_session == None:
        user_session = chat_session.create()

    response = ask_for_help(user, user_session, query)
    # response = {"output": "Welcome Emeka"}
    return Response({"reply": response["output"]}, status=status.HTTP_200_OK)


@api_view(["POST"])
def login_to_chat(request):
    email = request.data.get('email')
    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.filter(email=email).first()
    if user:
        token = Token.objects.filter(user_id=user.id).first()
        token.delete()
        token = Token.objects.create(user=user)
        chat_session = ChatSession(user)
        chat_session.create()
        return Response({"message": "Welcome back", "user_id": user.id, "token": token.key}, status=status.HTTP_200_OK)

    full_name = request.data.get('full_name')
    full_name_parts = full_name.split(" ")
    if len(full_name_parts) < 2:
        return Response({"error": "Full name must include both first and last name"}, status=status.HTTP_400_BAD_REQUEST)
    first_name = full_name_parts[0]
    last_name = full_name_parts[-1]

    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(
        username=email, email=email, first_name=first_name, last_name=last_name)
    token = Token.objects.create(user=user)
    chat_session = ChatSession(user)
    chat_session.create()

    return Response({"message": "User created successfully", "user_id": user.id, "token": token.key}, status=status.HTTP_201_CREATED)
