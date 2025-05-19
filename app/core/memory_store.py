from langgraph.checkpoint.memory import MemorySaver

memory_store = {}
def get_memory_for_user(user_id: int):
    if user_id not in memory_store:
        memory_store[user_id] = MemorySaver()
    return memory_store[user_id]