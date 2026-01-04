from typing import List, Literal, Any
# from langchain_core.tools import tool
# from langchain_core.messages import HumanMessage
from langchain_core.language_models import BaseLanguageModel
# from langchain_openai import ChatOpenAI
from typing import TypedDict
# from langgraph.prebuilt import create_react_agent
# from langchain_community.tools.tavily_search import TavilySearchResults
# from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import Command
from state import State

def make_supervisor_node(llm: BaseLanguageModel, members: List[str]) -> Any:
    """
     A factory function to create a supervisor node.
     This node routes to worker nodes based on the task and decide when to finish.
    """
    system_prompt = (
        "You are a supervisor tasked with managing a conversation between the"
        f" following workers: {members}. Given the following request,"
        " respond with the name of the worker to act next. Each worker will perform a"
        " task and respond with their results and status. When finished,"
        " respond with FINISH."
    )

    class Router(TypedDict):
        next: Literal["FINISH", *tuple(members)]

    def supervisor(state: State) -> Command:
        messages = [
            {"role": "system", "content": system_prompt}
        ] + state["messages"]

        response = llm.with_structured_output(Router).invoke(messages)
        goto = response["next"]
        return Command(goto=goto, update={"next": goto})

    return supervisor