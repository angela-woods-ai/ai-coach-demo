# Pinecone for storing reflection embeddings and retrieving the most relevant reflections

import os
import uuid
from .config import USE_PINECONE, PINECONE_API_KEY, PINECONE_INDEX_NAME, EMBED_DIM, SIMILARITY_THRESHOLD, RECREATE_PINECONE_INDEX
from .models import Reflection

# Config - Since it is paid use (or limited free use) only initialize if it is enabled
index = None
if USE_PINECONE:
    from pinecone import Pinecone, ServerlessSpec
    from pinecone.exceptions import NotFoundException

    assert PINECONE_API_KEY, "PINECONE_API_KEY not set"

    pc = Pinecone(api_key=PINECONE_API_KEY)

    # This happens when changing the EMBED_DIM size
    if(RECREATE_PINECONE_INDEX):
        if(pc.has_index(PINECONE_INDEX_NAME)):
            print("Deleting pinecone index")
            pc.delete_index(PINECONE_INDEX_NAME)

    existing = [i["name"] for i in pc.list_indexes()]

    if PINECONE_INDEX_NAME not in existing:
        print(f"Creating pinecone index {PINECONE_INDEX_NAME} Dim {EMBED_DIM}")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=EMBED_DIM,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1",
            ),
        )

    index = pc.Index(PINECONE_INDEX_NAME)

# Since I only have 1 demo user so far, I need to be able to clear that user when the clear call is made in the UI. 
def clear_user_pinecone(user_id: str):

    # Simple safeguard
    if not USE_PINECONE or index is None: return

    # Clear by metadata filter since user_id stored in the metadata
    try:
        index.delete(filter={"user_id": user_id})
    except NotFoundException:
        pass  # Namespace doesn't exist yet — safe to ignore. Happens on the first run on a fresh index when the namespace doesn't exist yet

# Store reflection embedding in Pinecone
def store_reflection_pinecone(user_id: str, reflection: Reflection):

    # Simple safeguard
    if not USE_PINECONE or index is None: return

    # # Create a pinecone only ID (unique per reflection & scoped to the user)
    # reflection_id = f"{user_id}-{uuid.uuid4()}"

    index.upsert(
        vectors=[{
            "id": reflection.embedding_id,
            "values": reflection.embedding,  # list[float]
            "metadata": {
                "user_id": user_id,
                "text": reflection.text,
                "timestamp": reflection.timestamp.isoformat(), 
                "embedding_id": reflection.embedding_id # Optional for now, since it is already stored in id
            }
        }]
    )

# Retrieve relevant reflections
def retrieve_relevant_reflections_pinecone(
    user_id: str,
    current_reflection: Reflection,
    k: int = 3,
    threshold: float = SIMILARITY_THRESHOLD
):
    # Simple safeguard
    if not USE_PINECONE or index is None: return []

    response = index.query(
        vector=current_reflection.embedding,
        top_k=k+1, # Ask for one extra so we get the desired number after filtering out current
        include_metadata=True,
        filter={
            "user_id": user_id
        }
    )

    relevant = []

    for match in response.get("matches", []):

        # Filter out the current reflection
        if match.id == current_reflection.embedding_id:
            continue

        # Only keep matches that meet the similarity threshold
        if(match.score >= threshold):
            metadata = match["metadata"]

            relevant.append(
                Reflection(
                    user_id=user_id,
                    text=metadata["text"],
                    timestamp=metadata["timestamp"],
                    embedding_id=metadata["embedding_id"],
                    embedding=None      # not needed for display
                )
            )

    return relevant

