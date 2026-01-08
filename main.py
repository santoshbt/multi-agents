import sys
from config import setup_environement


def main():
    setup_environement()

    # Import graph after environment is set so tools that rely
    # on env vars initialize correctly.
    from agents.main_graph import super_graph

    if len(sys.argv) > 1:
        query = "  ".join(sys.argv[1:])
    else:
        print("Please provide a query as a command-line argument.")
        print('Example: python main.py "What is the capital of France?"')
        return

    print(f"Executing query: {query}\n")

    initial_state = {"messages": [("user", query)]}

    # Use thread_id to maintain conversation history
    # Different thread_ids = different conversations
    config = {"configurable": {"thread_id": "default_conversation"}}

    for s in super_graph.stream(
        initial_state,
        config=config,
        stream_mode="values"
    ):
        if "__end__" not in s:
            print(s)
            print("--------------------------")

if __name__ == "__main__":
    main()