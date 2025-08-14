from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from django.contrib.auth.models import User


from .prompt_template import FLIGHT_AGENT_TEMPLATE
from .pg_vector_interface import (vector_store)
from .chat_history import ChatHistory
from .tools import generate_flight_tools

load_dotenv()


def get_agent_context(query_text: str):
    results = vector_store.similarity_search(query_text)

    return "\n\n---\n\n".join([doc.page_content for doc in results])


def invoke_agent(query_text: str, user: User, external_user_id: str) -> dict:
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    chat_history = ChatHistory(session_id=external_user_id)
    messages = chat_history.get_messages()
    tools = generate_flight_tools(user)

    context_text = get_agent_context(query_text)
    prompt_template = ChatPromptTemplate.from_template(FLIGHT_AGENT_TEMPLATE)
    system = prompt_template.format(context=context_text)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    agent = create_tool_calling_agent(llm, tools, prompt)

    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    print(executor)
    response = executor.invoke({"query": query_text, "chat_history": messages})

    chat_history.add_message("human", query_text)
    chat_history.add_message("ai", response["output"])
    print(f"Response: {response}")
    return response
