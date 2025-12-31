# In memory storage (Mock database)

from collections import defaultdict
from .models import Reflection
from .config import USE_PINECONE


# Temporary in-memory store later could be postgress
# list of reflections per user_id
# For now this is my "ground truth" and pinecone is a derived store
USER_REFLECTIONS = defaultdict(list)
# Temporary storage for where compressed reflections go (longer term memory)
# Holds current and a history of summaries per user_id
# as a USER_MEMORY_SUMMARIES = {
#     user_id: {
#         "current": MemorySummary,
#         "history": [MemorySummary, ...]
#     }
# }
# Later storage could look like
# Postgres: summaries table
# ClickHouse: summary evolution analytics
# Pinecone: summary embeddings
USER_MEMORY_SUMMARIES = {}
# Use a small window for updating memories to see it working with a small number of reflections
MEMORY_UPDATE_WINDOW = 3

def init_user_memory(user_id):
    if user_id not in USER_MEMORY_SUMMARIES:
        USER_MEMORY_SUMMARIES[user_id] = {
            "current": None,
            "history": []
        }

# Set up for simple demo with only one user that gets cleared as needed
def clear_user_state(user_id):
    USER_REFLECTIONS[user_id] = []
    USER_MEMORY_SUMMARIES[user_id] = {
        "current": None,
        "history": []
    }
    if USE_PINECONE:
        # Import here so that pinecone only initializes if the flag is on
        from .vector_store import clear_user_pinecone
        # Clear pinecone for that user
        clear_user_pinecone(user_id)

def store_reflection(user_id: str, reflection: Reflection) -> None:
    USER_REFLECTIONS[user_id].append(reflection)

    if USE_PINECONE:
        # Import here so that pinecone only initializes if the flag is on
        from .vector_store import store_reflection_pinecone

        # Store the embedding of the reflection in pinecone
        store_reflection_pinecone(user_id, reflection)

def get_recent_reflections(user_id: str, limit: int = 5) -> list[Reflection]:
    # Getting the lastn n reflections
    return USER_REFLECTIONS[user_id][-limit:]   

