
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


from ..prompt_template import VOICE_TO_TEXT_TEMPLATE
from ..agent_advance import AdvanceAgent


def get_prompt_template():
    return ChatPromptTemplate.from_messages([
        ("system",  VOICE_TO_TEXT_TEMPLATE),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}")
    ])


def correct_text(query: str,) -> dict:
    advance_executor = AdvanceAgent(
        get_prompt_template(),
        [],
        ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    )

    response = advance_executor.agent_executor.invoke(
        {"query": query})

    return response
