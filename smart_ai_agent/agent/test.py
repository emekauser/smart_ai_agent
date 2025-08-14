from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()


@tool
def my_configurable_tool(input_data: str, config: RunnableConfig) -> str:
    """
    A tool that demonstrates accessing configuration during execution.
    """
    session_id = config.get("configurable", {}).get("session_id")
    # You can access other config values as needed
    return f"Processed '{input_data}' with session_id: {session_id}"


llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")


llm_with_tools = llm.bind_tools([my_configurable_tool])

chain = {"input_data": RunnablePassthrough(
)} | llm_with_tools | StrOutputParser()

result_chain = chain.invoke({"input_data": "another data"}, config={
                            "configurable": {"session_id": "def456uvw"}})
print(result_chain)
