"""
In-memory conversation history storage for private chats and groups.

Note: This is process-local, in-memory storage (matching the original
bot's behavior). History is lost on restart and is not shared across
multiple bot instances.
"""

from app.config import MAX_MEMORY

# Per-user private memory: {user_id: [{"role": ..., "content": ...}, ...]}
_private_memory: dict[int, list[dict]] = {}

# Per-group shared memory: {chat_id: [{"role": ..., "content": ...}, ...]}
_group_memory: dict[int, list[dict]] = {}


def get_private_history(user_id: int) -> list[dict]:
    """Return the stored conversation history for a private chat user."""
    return _private_memory.get(user_id, [])


def save_private(user_id: int, role: str, content: str) -> None:
    """Append a message to a user's private conversation history.

    Trims the history to the most recent MAX_MEMORY entries.
    """
    if user_id not in _private_memory:
        _private_memory[user_id] = []
    _private_memory[user_id].append({"role": role, "content": content})
    if len(_private_memory[user_id]) > MAX_MEMORY:
        _private_memory[user_id] = _private_memory[user_id][-MAX_MEMORY:]


def get_group_history(chat_id: int) -> list[dict]:
    """Return the stored shared conversation history for a group chat."""
    return _group_memory.get(chat_id, [])


def save_group(chat_id: int, role: str, content: str) -> None:
    """Append a message to a group's shared conversation history.

    Trims the history to the most recent MAX_MEMORY entries.
    """
    if chat_id not in _group_memory:
        _group_memory[chat_id] = []
    _group_memory[chat_id].append({"role": role, "content": content})
    if len(_group_memory[chat_id]) > MAX_MEMORY:
        _group_memory[chat_id] = _group_memory[chat_id][-MAX_MEMORY:]


def clear_private(user_id: int) -> None:
    """Clear a user's private conversation history."""
    _private_memory[user_id] = []


def clear_group(chat_id: int) -> None:
    """Clear a group's shared conversation history."""
    _group_memory[chat_id] = []
