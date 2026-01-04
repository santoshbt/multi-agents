# Multi-Agent Research and Writing System

A sophisticated multi-agent system powered by LangGraph and OpenAI that coordinates specialized teams to perform research and content creation tasks. The system uses a hierarchical supervisor architecture to orchestrate multiple AI agents, each with specific capabilities and tools.

## Overview

This application implements a multi-agent workflow where a top-level supervisor coordinates between two specialized teams:

- **Research Team**: Handles web searching and scraping to gather information
- **Writing Team**: Creates outlines and writes documents based on research findings

Each team has its own supervisor that manages sub-agents with specific tools, creating an efficient and organized workflow for complex tasks.

## Architecture

```
Super Supervisor
    ├── Research Team Supervisor
    │   ├── Search Agent (Tavily Search)
    │   └── Web Scraper Agent (Web Scraping)
    │
    └── Writing Team Supervisor
        ├── Note Taker Agent (Outline Creation)
        └── Document Writer Agent (Document Creation/Editing)
```

## Features

- **Hierarchical Multi-Agent System**: Two-level supervisor architecture for complex task coordination
- **Specialized Agents**: Each agent has specific tools and responsibilities
- **Web Research**: Integrated Tavily search and web scraping capabilities
- **Document Management**: Create outlines, write, read, and edit documents
- **State Management**: Shared state across all agents using LangGraph
- **Flexible Routing**: Dynamic routing based on task requirements

## Prerequisites

- Python 3.13+
- OpenAI API key
- Tavily API key (for web search)

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd multi-agents
```

2. Create and activate a virtual environment:
```bash
python -m venv multi-agents
# On Windows
multi-agents\Scripts\activate
# On Unix or MacOS
source multi-agents/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your API keys:
```env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

## Usage

Run the application with a query from the command line:

```bash
python main.py "Your query here"
```

### Example Queries

```bash
# Research and write about a topic
python main.py "Research current trends in AI and write a summary"

# Create content with research
python main.py "Find information about climate change and create an outline for a report"

# Complex research task
python main.py "Search for recent developments in quantum computing and write a detailed article"
```

## Components

### Agents

#### Research Team
- **Search Agent**: Uses Tavily API to perform web searches
- **Web Scraper Agent**: Scrapes and extracts content from web pages

#### Writing Team
- **Note Taker Agent**: Creates structured outlines for documents
- **Document Writer Agent**: Writes, reads, and edits documents

### Tools

#### Web Tools
- `tavily_tool`: Performs web searches using Tavily API (max 3 results)
- `scrape_webpages`: Scrapes content from provided URLs

#### File Tools
- `create_outline`: Creates and saves outline files
- `read_document`: Reads document content (with optional line range)
- `write_document`: Writes content to a new document
- `edit_document`: Edits existing documents by inserting text at specific lines

### Configuration

The system uses GPT-4o as the default model. You can modify this in [config.py](config.py):

```python
llm = ChatOpenAI(model="gpt-4o")
```

## How It Works

1. **User Query**: You provide a query via command line
2. **Super Supervisor**: Analyzes the query and routes to the appropriate team
3. **Team Execution**:
   - Research team gathers information if needed
   - Writing team creates outlines and documents
4. **Coordination**: Teams communicate back to the supervisor
5. **Completion**: Process continues until the task is complete (supervisor returns "FINISH")

## Output

Generated documents are saved in the `temp/` directory with filenames specified by the agents during execution.

## Dependencies

- `langchain` - LangChain framework
- `langchain-openai` - OpenAI integration
- `langgraph` - Graph-based agent orchestration
- `langchain-community` - Community tools (Tavily, web scraping)
- `python-dotenv` - Environment variable management
- See [requirements.txt](requirements.txt) for complete list

## Configuration Options

Modify the recursion limit in [main.py](main.py):

```python
super_graph.stream(initial_state, {"recursion_limit": 30})
```

## Troubleshooting

- **Missing API Keys**: Ensure your `.env` file contains valid `OPENAI_API_KEY` and `TAVILY_API_KEY`
- **Module Not Found**: Verify all dependencies are installed: `pip install -r requirements.txt`
- **Permission Errors**: Check that the `temp/` directory is writable

## Contributing

Feel free to submit issues and enhancement requests!

## License

[Add your license information here]

## Acknowledgments

Built with:
- [LangChain](https://github.com/langchain-ai/langchain)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [OpenAI](https://openai.com/)
- [Tavily](https://tavily.com/)