"""
Utility functions for working with memory/checkpointing in the multi-agent system.
"""

from agents.main_graph import super_graph


def get_conversation_history(thread_id: str):
    """
    Retrieve the conversation history for a specific thread.

    Args:
        thread_id: The thread identifier

    Returns:
        The state history for the conversation
    """
    config = {"configurable": {"thread_id": thread_id}}
    state = super_graph.get_state(config)
    return state


def list_all_conversations():
    """
    List all available conversation threads in the checkpoint store.

    Returns:
        List of conversation states
    """
    # Get all checkpoints
    checkpoints = super_graph.checkpointer.list(config=None)
    return list(checkpoints)


def continue_conversation(thread_id: str, new_message: str):
    """
    Continue an existing conversation by adding a new message.

    Args:
        thread_id: The thread identifier to continue
        new_message: The new user message to add

    Returns:
        The updated state after processing the message
    """
    config = {"configurable": {"thread_id": thread_id}}

    # Add new message to existing thread
    result = super_graph.invoke(
        {"messages": [("user", new_message)]},
        config=config
    )

    return result


def clear_conversation(thread_id: str):
    """
    Clear/delete a specific conversation thread.
    Note: Implementation depends on checkpointer type.

    Args:
        thread_id: The thread identifier to clear
    """
    # For SQLite, you would need to manually delete from the database
    # This is a placeholder - actual implementation varies
    print(f"To clear conversation {thread_id}, delete from the checkpoints.db")


def get_message_count(thread_id: str):
    """
    Get the number of messages in a conversation thread.

    Args:
        thread_id: The thread identifier

    Returns:
        Number of messages in the thread
    """
    state = get_conversation_history(thread_id)
    if state and state.values:
        return len(state.values.get("messages", []))
    return 0


# Example usage
if __name__ == "__main__":
    from config import setup_environement
    setup_environement()

    # Example: Get history for default conversation
    history = get_conversation_history("default_conversation")
    print(f"Current state: {history}")

    # Example: Continue a conversation
    # result = continue_conversation("default_conversation", "What did we discuss earlier?")
    # print(result)
