from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.tools import Tool

load_dotenv()


class AdvanceAgent:

    def __init__(self, prompt_template: ChatPromptTemplate, tools: list[Tool], model):
        self.model = model
        self.tools = tools
        self.prompt_template = prompt_template
        self.build()

    def build(self):
        print(self.tools)
        agent = create_tool_calling_agent(
            self.model, self.tools,  self.prompt_template)

        self.agent_executor = AgentExecutor(
            agent=agent, tools=self.tools, verbose=True)

    # @classmethod
    # def create_with_tools(cls, user: User, prompt_template: str, tools: list[Tool], model):
    #     instance = cls(user)
    #     chat_history = ChatHistoryV1(session_id=user.userdata.external_id)
    #     instance.model = model
    #     instance.tools = tools
    #     prompt = instance.prompt(
    #         prompt_template=prompt_template, state=chat_history)
    #     instance.agent = create_react_agent(
    #         model=model,
    #         tools=tools,
    #         prompt=prompt,
    #     )

    #     return instance

    # @classmethod
    # def create_agent(cls, user: User, prompt_template: str, model):
    #     cls.create_with_tools(
    #         user=user, prompt_template=prompt_template, tools=[], model=model)
