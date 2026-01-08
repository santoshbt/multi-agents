# Memory Persistence Implementation Guide

## Overview

This multi-agent system now supports memory persistence using LangGraph's checkpointing feature. This allows conversations to be saved and resumed, maintaining context across multiple interactions.

## Installation

First, install the new dependency:

```bash
pip install -r requirements.txt
```

Or install directly:
```bash
pip install langgraph-checkpoint-sqlite
```

## How It Works

### Checkpointing
- Every interaction is automatically saved to a SQLite database (`checkpoints.db`)
- Each conversation is identified by a unique `thread_id`
- The complete state (including all messages) is persisted

### Thread IDs
- **Thread ID**: A unique identifier for each conversation
- Different thread_ids = separate conversations with independent histories
- Same thread_id = continued conversation with shared context

## Usage

### Option 1: Original Script (Simple)

Use `main.py` for basic usage with a default thread:

```bash
python main.py "Research the latest AI trends"
```

All conversations use the thread_id: `"default_conversation"`

### Option 2: Enhanced Script (Recommended)

Use `main_with_memory.py` for advanced memory features:

#### Start a new conversation
```bash
python main_with_memory.py "Research gold price trends"
# Creates thread: conversation_20260108_143022
```

#### Continue a specific conversation
```bash
python main_with_memory.py --thread conversation_20260108_143022 "What were your key findings?"
```

#### List all conversations
```bash
python main_with_memory.py --list
```

#### View conversation history
```bash
python main_with_memory.py --history conversation_20260108_143022
```

## Memory Utilities

The `memory_utils.py` file provides helper functions:

```python
from memory_utils import (
    get_conversation_history,
    continue_conversation,
    get_message_count,
    list_all_conversations
)

# Get history for a thread
history = get_conversation_history("my_thread_id")

# Continue a conversation programmatically
result = continue_conversation("my_thread_id", "Follow-up question")

# Get message count
count = get_message_count("my_thread_id")
```

## Storage Options

### Current: SQLite (Local Storage)
- **File**: `checkpoints.db` (created automatically)
- **Pros**: Simple, no setup required, persistent across runs
- **Cons**: Local only, not suitable for distributed systems

### Alternative Options

#### PostgreSQL (Production)
For production environments with multiple workers:

```python
from langgraph.checkpoint.postgres import PostgresSaver

# In agents/main_graph.py
memory = PostgresSaver.from_conn_string("postgresql://user:pass@localhost/dbname")
super_graph = super_builder.compile(checkpointer=memory)
```

Install: `pip install langgraph-checkpoint-postgres psycopg2-binary`

#### In-Memory (Testing)
For testing without persistence:

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
super_graph = super_builder.compile(checkpointer=memory)
```

## State Management

The current state includes:
- All messages in the conversation
- The `next` field for routing decisions
- Any additional state defined in `state.py`

To add more persistent data, extend the `State` class:

```python
# In state.py
from langgraph.graph import MessagesState
from typing import List

class State(MessagesState):
    next: str
    research_notes: List[str] = []  # Persists research findings
    document_versions: dict = {}     # Tracks document iterations
```

## Advanced Features

### Time Travel
Access previous checkpoints:

```python
from agents.main_graph import super_graph

config = {"configurable": {"thread_id": "my_thread"}}

# Get current state
current_state = super_graph.get_state(config)

# Get state history
history = super_graph.get_state_history(config)
for state in history:
    print(f"Checkpoint: {state.checkpoint}")
    print(f"Messages: {len(state.values['messages'])}")
```

### Branching Conversations
Create alternate paths from a checkpoint:

```python
# Get state at specific checkpoint
config = {
    "configurable": {
        "thread_id": "my_thread",
        "checkpoint_id": "specific_checkpoint_id"
    }
}

# Continue from that point with different input
result = super_graph.invoke({"messages": [("user", "Alternative question")]}, config)
```

## Cleanup

To clear old conversations:

```bash
# Delete the database file
rm checkpoints.db  # Linux/Mac
del checkpoints.db  # Windows
```

Or implement selective deletion in your code.

## Best Practices

1. **Use descriptive thread_ids**: Makes it easier to track conversations
2. **Implement cleanup**: Periodically delete old checkpoints to save space
3. **Monitor storage**: SQLite files can grow large with many conversations
4. **Consider privacy**: Sensitive data is stored in plaintext in the database
5. **Backup important threads**: Copy `checkpoints.db` for important conversations

## Troubleshooting

### Database locked error
- Ensure only one process accesses the database at a time
- Consider switching to PostgreSQL for concurrent access

### Memory too large
- Implement message trimming in your state
- Periodically clean up old threads

### Lost context
- Verify you're using the correct thread_id
- Check that checkpoints.db exists and is accessible

## Example Workflow

```bash
# Day 1: Start research
python main_with_memory.py "Research AI safety concerns"
# Output: conversation_20260108_100000

# Day 2: Continue research
python main_with_memory.py --thread conversation_20260108_100000 "What are the top 3 concerns?"

# Day 3: Write article based on research
python main_with_memory.py --thread conversation_20260108_100000 "Write an article about our findings"

# Check history
python main_with_memory.py --history conversation_20260108_100000
```
