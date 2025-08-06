from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from .prompt_template import PROMPT_TEMPLATE_1
from .pg_vector_interface import (vector_store)
from .chat_history import ChatHistory

load_dotenv()

def get_agent_context(query_text: str):
    results = vector_store.similarity_search(query_text)

    return "\n\n---\n\n".join([doc.page_content for doc in results])

def invoke_agent(query_text: str):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    chat_history = ChatHistory(session_id="7cddff78-60a6-4b72-8fde-9a1d3c2a2e53")
    messages = chat_history.get_messages()

    context_text = get_agent_context(query_text)
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_1)
    system = prompt_template.format(context=context_text, question=query_text)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    agent = create_tool_calling_agent(llm, [], prompt)
    executor = AgentExecutor(agent=agent, tools=[], verbose=True)
    response = executor.invoke({"query": query_text, "chat_history": messages})

    chat_history.add_message("human", query_text)
    chat_history.add_message("ai", response["output"])

    return response

