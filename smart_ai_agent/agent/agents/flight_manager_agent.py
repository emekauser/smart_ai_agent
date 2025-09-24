
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from ..prompt_template import FLIGHT_AGENT_TEMPLATE
from ..pg_vector_interface_async import VectorStoreInterface
from ..chat_history import ChatHistoryV1
from ..agent_advance import AdvanceAgent
from ..tools import generate_flight_tools
from ..agent_models import get_model
from api.models import UserChatSession


async def get_agent_context(query_text: str):
    vector_interface = await VectorStoreInterface.connect()
    results = await vector_interface.search_documents(query_text)

    return "\n\n---\n\n".join([doc.page_content for doc in results])


def get_prompt_template(context_text: str, user: User):
    prompt_template = ChatPromptTemplate.from_template(FLIGHT_AGENT_TEMPLATE)
    system = prompt_template.format(
        context=context_text, first_name=user.first_name, email=user.email, surname=user.last_name)

    return ChatPromptTemplate.from_messages([
        ("system",  system),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}")
    ])


def ask_for_help(user: User, user_chat_session: UserChatSession, query: str,) -> dict:
    context_text = async_to_sync(get_agent_context)(query)
    print(user_chat_session)
    chat_history = ChatHistoryV1(session_id=user_chat_session.session_id)
    tools = generate_flight_tools(user)

    advance_executor = AdvanceAgent(
        get_prompt_template(context_text, user),
        tools,
        ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    )

    response = advance_executor.agent_executor.invoke(
        {"query": query, "chat_history": chat_history.get_messages()})

    chat_history.add_message("human", query)
    chat_history.add_message("ai", response["output"])
    return response
