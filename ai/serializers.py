# Serialize into Data Transfer Objects

from datetime import datetime
from .api_types import (
    ReflectionDTO,
    CoachingContextDTO,
    CoachingResponseDTO,
    ProcessReflectionResultDTO
)

# Serialize Reflection to ReflectionDTO
def reflection_to_dto(reflection):
    ts = reflection.timestamp

    if isinstance(ts, datetime):
        timestamp_str = ts.isoformat()
    elif isinstance(ts, str):
        timestamp_str = ts
    else:
        raise TypeError(f"Unexpected timestamp type: {type(ts)}")

    return ReflectionDTO(
        text=reflection.text,
        timestamp=timestamp_str,
        embedding_id=reflection.embedding_id
    )

# Serialize ProcessReflectionResult into ProcessReflectionResultDTO
def serialize_process_reflection_result(result):
    domain_context = result.context

    return ProcessReflectionResultDTO(
        context=CoachingContextDTO(
            current_reflection=reflection_to_dto(
                domain_context.current_reflection
            ),
            relevant_reflections=[
                reflection_to_dto(r)
                for r in domain_context.relevant_reflections
            ],
            memory_summary=(
                domain_context.memory_summary_current.summary_text
                if domain_context.memory_summary_current else None
            )
        ),
        coaching=(
            CoachingResponseDTO(
                message=result.response.message,
                follow_up_questions=result.response.follow_up_questions
            )
            if result.response else None
        ),
        memory_updated = result.memory_updated,
        reflection_count = result.reflection_count
    )
