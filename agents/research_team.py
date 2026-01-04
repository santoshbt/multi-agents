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
from tools.web_tools import tavily_tool, scrape_webpages
from langgraph.graph import START

search_agent = create_react_agent(llm, tools=[tavily_tool])
def search_node(state: State) -> Command[Literal["supervisor"]]:
    result = search_agent.invoke(state)
    return Command(
        update={
            "messages": [HumanMessage(content=result["messages"][-1].content, name="search")]
        },
        goto="supervisor"
    )

web_scraper_agent = create_react_agent(llm, tools=[scrape_webpages])
def web_scraper_node(state: State) -> Command[Literal["supervisor"]]:
    result = web_scraper_agent.invoke(state)
    return Command(
        update={
            "messages": [HumanMessage(content=result["messages"][-1].content, name="web_scraper")]
        },
        goto="supervisor"
    )

research_supervisor_node = make_supervisor_node(llm, members=["search", "web_scraper"])

research_builder = StateGraph(State)
research_builder.add_node("supervisor", research_supervisor_node)
research_builder.add_node("search", search_node)
research_builder.add_node("web_scraper", web_scraper_node)

research_builder.add_edge(START, "supervisor")
research_graph = research_builder.compile()