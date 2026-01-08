"""
Enhanced main script with support for conversation threads and memory.

Usage:
    # New conversation (auto-generates thread_id)
    python main_with_memory.py "Your query here"

    # Continue specific conversation
    python main_with_memory.py --thread my_thread_id "Your query here"

    # List all conversations
    python main_with_memory.py --list

    # Show history of a thread
    python main_with_memory.py --history my_thread_id
"""

import sys
import argparse
from datetime import datetime
from config import setup_environement


def main():
    setup_environement()

    # Import graph after environment is set
    from agents.main_graph import super_graph
    from memory_utils import get_conversation_history, list_all_conversations

    parser = argparse.ArgumentParser(description='Multi-agent system with memory')
    parser.add_argument('query', nargs='*', help='The query to process')
    parser.add_argument('--thread', type=str, help='Thread ID for conversation continuity')
    parser.add_argument('--list', action='store_true', help='List all conversation threads')
    parser.add_argument('--history', type=str, help='Show history for a specific thread')

    args = parser.parse_args()

    # Handle list command
    if args.list:
        print("Available conversation threads:")
        conversations = list_all_conversations()
        for conv in conversations:
            print(f"  - Thread ID: {conv.config['configurable']['thread_id']}")
            print(f"    Checkpoint: {conv.checkpoint}")
        return

    # Handle history command
    if args.history:
        print(f"History for thread '{args.history}':")
        state = get_conversation_history(args.history)
        if state and state.values:
            messages = state.values.get("messages", [])
            for i, msg in enumerate(messages):
                print(f"\n[{i+1}] {type(msg).__name__}:")
                print(f"    {msg.content}")
        else:
            print("No history found for this thread.")
        return

    # Handle query
    if not args.query:
        print("Please provide a query.")
        print('Example: python main_with_memory.py "What is the capital of France?"')
        print('Or use: python main_with_memory.py --help')
        return

    query = " ".join(args.query)

    # Determine thread_id
    if args.thread:
        thread_id = args.thread
        print(f"Continuing conversation in thread: {thread_id}")
    else:
        # Generate new thread_id with timestamp
        thread_id = f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print(f"Starting new conversation with thread: {thread_id}")

    print(f"Executing query: {query}\n")

    initial_state = {"messages": [("user", query)]}
    config = {"configurable": {"thread_id": thread_id}}

    for s in super_graph.stream(
        initial_state,
        config=config,
        stream_mode="values"
    ):
        if "__end__" not in s:
            print(s)
            print("--------------------------")

    print(f"\n✓ Conversation saved to thread: {thread_id}")
    print(f"To continue this conversation, use: --thread {thread_id}")


if __name__ == "__main__":
    main()
