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

    for s in super_graph.stream(
        initial_state,
        {"recursion_limit": 30}
    ):
        if "__end__" not in s:
            print(s)
            print("--------------------------")

if __name__ == "__main__":
    main()