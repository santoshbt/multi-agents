from typing import Literal
# from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
# from langchain_core.language_models import BaseLanguageModel
# from langchain_openai import ChatOpenAI
# from typing import TypedDict
from langgraph.prebuilt import create_react_agent
# from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, START
from langgraph.types import Command
from state import State
from supervisor import make_supervisor_node
from config import llm
from tools.file_tools import write_document, read_document, edit_document, create_outline

doc_writer_agent = create_react_agent(
    llm,
    tools = [write_document, edit_document, read_document],
)
def doc_writing_node(state: State) -> Command[Literal["supervisor"]]:
    result = doc_writer_agent.invoke(state)
    return Command(
        update = {
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="doc_writer")
            ]
        },
        goto = "supervisor"
    )

note_taking_agent = create_react_agent(
    llm,
    tools = [create_outline, read_document],
)

def note_taking_node(state: State) -> Command[Literal["supervisor"]]:
    result = note_taking_agent.invoke(state)
    return Command(
       update = {
           "messages": [
               HumanMessage(content=result["messages"][-1].content, name="note_taker")
           ]
       },
       goto = "supervisor"
    )

writing_supervisor_node = make_supervisor_node(
    llm, members = ["doc_writer", "note_taker"]
)

writing_builder = StateGraph(State)
writing_builder.add_node("supervisor", writing_supervisor_node)
writing_builder.add_node("doc_writer", doc_writing_node)
writing_builder.add_node("note_taker", note_taking_node)
# writing_builder.add_node("chart_generator", chart_generating_node)

writing_builder.add_edge("doc_writer", "supervisor")
writing_builder.add_edge("note_taker", "supervisor")

# Entrypoint for the writing graph: start at the supervisor node
writing_builder.add_edge(START, "supervisor")

writing_graph = writing_builder.compile()
