import getpass
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

def setup_environement():
    """ Sets up API keys from environment variables if not already set. """
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")


# Centralized LLM instance
llm = ChatOpenAI(model="gpt-4o")