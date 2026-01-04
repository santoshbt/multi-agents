from typing import Literal
# from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
# from langchain_core.language_models import BaseLanguageModel
# from langchain_openai import ChatOpenAI
# from typing import TypedDict
from langgraph.prebuilt import create_react_agent
# from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph
from langgraph.types import Command
from state import State
from supervisor import make_supervisor_node
from config import llm
from .research_team import research_graph
from .writing_team import writing_graph
from langgraph.graph import START, END


teams_supervisor_node = make_supervisor_node(llm, ["research_team", "writing_team"])

def call_research_team(state: State) -> Command[Literal["supervisor"]]:
    result = research_graph.invoke({"messages": state["messages"][-1]})
    return Command(
        update={
            "messages": [HumanMessage(content=result["messages"][-1].content, name="research_team")]
        },
        goto="supervisor"
    )

def call_writing_team(state: State) -> Command[Literal["supervisor"]]:
    result = writing_graph.invoke({"messages": state["messages"][-1]})
    return Command(
        update={
            "messages": [HumanMessage(content=result["messages"][-1].content, name="writing_team")]
        },
        goto="supervisor"
    )

def route_teams(state: State) -> str:
    """Route based on supervisor's next field"""
    if state.get("next") == "FINISH":
        return END
    return state.get("next", "supervisor")

super_builder = StateGraph(State)
super_builder.add_node("supervisor", teams_supervisor_node)
super_builder.add_node("research_team", call_research_team)
super_builder.add_node("writing_team", call_writing_team)

super_builder.add_edge(START, "supervisor")
super_builder.add_conditional_edges(
    "supervisor",
    route_teams,
    {"research_team": "research_team", "writing_team": "writing_team", END: END}
)
super_builder.add_edge("research_team", "supervisor")
super_builder.add_edge("writing_team", "supervisor")

super_graph = super_builder.compile()