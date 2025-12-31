# Python ↔ Node contract (dataclasses)
# Currently these are all UI facing DTOs

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class ReflectionDTO:
    # user_id deliberately not included so it doesn't leak to the UI that currently has only one user 
    text: str
    timestamp: str
    embedding_id: str # ID for embedding vector
    
@dataclass
class CoachingContextDTO:
    current_reflection: ReflectionDTO
    relevant_reflections: List[ReflectionDTO]
    memory_summary: Optional[str]

@dataclass
class CoachingResponseDTO:
    message: str
    follow_up_questions: List[str]

@dataclass
class ProcessReflectionResultDTO:
    context: CoachingContextDTO
    coaching: Optional[CoachingResponseDTO]
    memory_updated: bool
    reflection_count: int

