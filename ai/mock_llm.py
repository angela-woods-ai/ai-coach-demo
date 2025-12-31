# Coach message generation (mocked)

from .models import Reflection
from .state import USER_MEMORY_SUMMARIES
from .models import CoachingContext, CoachingResponse

# Intentionally dumb, can be used for system testing to control cost of real llm
def mock_llm_coach_response(context: CoachingContext) -> CoachingResponse:
    message_parts = []

    # Acknowledge the present
    message_parts.append(
        f"You shared today: '{context.current_reflection.text}'."
    )

    referenced_memories = []

    # Use current belief
    if context.memory_summary_current:
        message_parts.append(
             f"Looking across time, {context.memory_summary_current.summary_text}"
        )
        referenced_memories.append(context.memory_summary_current.summary_text)

    if context.relevant_reflections:
        message_parts.append(
            f"This connects with {len(context.relevant_reflections)} similar moments."
        )
        referenced_memories.extend(
            r.text for r in context.relevant_reflections
        )

    follow_ups = [
        "What feels most important to explore right now?",
        # "What support would help you move forward?"
    ]        
    
    return CoachingResponse(
        message="\n".join(message_parts),
        follow_up_questions=follow_ups,
        referenced_memories=referenced_memories,
        confidence=0.6,  # mock
        model_info={
            "provider": "mock",
            "model": "rule-based-v1"
        }
    )    
