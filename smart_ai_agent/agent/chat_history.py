from langchain_core.messages import AIMessage, HumanMessage
from langchain_postgres import PostgresChatMessageHistory
from dotenv import load_dotenv
import os
import psycopg

load_dotenv()
db_name =  os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
if not db_name or not db_user or not db_password or not db_host:
    raise ValueError("Database connection details are not set in the environment variables.")

CONNECTION= f"dbname={db_name} user={db_user} password={db_password} host={db_host}"
sync_connection = psycopg.connect(CONNECTION)
table_name = "chat_history"
PostgresChatMessageHistory.create_tables(sync_connection, table_name)

class ChatHistory:
    session_id = str("7cddff78-60a6-4b72-8fde-9a1d3c2a2e52")  # Unique identifier for the chat session

    def __init__(self, session_id: str):
        self.session_id = session_id

        # Initialize the chat history manager
        self.chat_history = PostgresChatMessageHistory(
            table_name,
            session_id,
            sync_connection=sync_connection
        )

    def add_message(self, role: str, content: str):
        """
        Add a message to the chat history.
        """
        if role == "human":
            message = HumanMessage(content=content)
        elif role == "ai":
            message = AIMessage(content=content)
        else:
            message = None
            
        if message:
            self.chat_history.add_message(message)

    def get_messages(self) -> list[AIMessage | HumanMessage]:
        """
        Retrieve all messages from the chat history.
        Returns a list of messages.
        """
        return self.chat_history.messages[:10]  # Limit to the last 10 messages
