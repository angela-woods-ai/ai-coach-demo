# Orchestration logic (core brain)

from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import uuid
from .models import Reflection, CoachingContext, CoachingResponse
from .state import store_reflection, MEMORY_UPDATE_WINDOW, USER_MEMORY_SUMMARIES, get_recent_reflections
from .memory import summarize_reflections
from .mock_llm import mock_llm_coach_response
from .llm.claude_client import claude_coach
from .retrieval import embed_text, retrieve_relevant_reflections
from .config import EMBED_DIM, USE_CLAUDE

@dataclass
class ProcessReflectionResult:
    context: CoachingContext
    response: Optional[CoachingResponse]
    memory_updated: bool
    reflection_count: int

# Create the coach response from the context
def coach_response(context: CoachingContext) -> CoachingResponse:
    if USE_CLAUDE:
        # Real LLM (current cost is fractions of a cent per reflection)
        return claude_coach(context)
        
    # Otherwise mock the response
    return mock_llm_coach_response(context)
    

# Build a personalized context that can uses the most relevant reflections to the current one.
def build_coaching_context(user_id: str, new_reflection: Reflection, history_limit: int = 3) -> CoachingContext:
    recent_reflections = get_recent_reflections(user_id, history_limit)

    relevant_reflections = retrieve_relevant_reflections(user_id, new_reflection)

    memory_summary = USER_MEMORY_SUMMARIES.get(
        user_id,
        {"current": None, "history": []}
    )

    return CoachingContext(
        user_id=user_id,
        current_reflection=new_reflection,
        recent_reflections=recent_reflections,
        relevant_reflections=relevant_reflections,
        memory_summary_current=memory_summary["current"],
        memory_summary_history=memory_summary["history"]
    )

# Process one user reflection
def process_reflection(user_id: str, idx: int, text: str):
    print(f"[USER_REFLECTION:{idx}: {text}")

    memory_updated = False

    # Create the reflection
    reflection = Reflection(
        user_id=user_id,
        text=text,
        timestamp=datetime.now(),
        embedding=embed_text(text, EMBED_DIM),
        embedding_id = f"{user_id}-{uuid.uuid4()}" # Create an id that is useful to use with pinecone (unique per reflection & scoped to the user)
    )

    # Store the reflection
    store_reflection(user_id, reflection)

    # Update summarized memory periodically
    if idx % MEMORY_UPDATE_WINDOW == 0:
        recent = get_recent_reflections(user_id, MEMORY_UPDATE_WINDOW)
        summary = summarize_reflections(recent)
        if summary:
            USER_MEMORY_SUMMARIES[user_id]["history"].append(summary)
            USER_MEMORY_SUMMARIES[user_id]["current"] = summary
            memory_updated = True

    # for now, create context & build the response each time, that can change later if we don't want a coaching response for every reflection
    context = build_coaching_context(user_id, reflection)
    response = coach_response(context)

    # Create the response object
    return ProcessReflectionResult(
        context=context,
        response=response,
        memory_updated = memory_updated,
        reflection_count = idx
    )