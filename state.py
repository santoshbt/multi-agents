from langgraph.graph import MessagesState

class State(MessagesState):
    """
    The shared state for the agent graphs.

    Attributes:
        next(str): The next node to execute
    """
    next: str