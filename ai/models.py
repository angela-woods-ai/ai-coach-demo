# Pure data classes

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Reflection:
    user_id: str
    text: str
    timestamp: datetime
    embedding: list[float] # Type for using with hash trick embeddings
    embedding_id: str # Embedding ID for use with Pinecone

@dataclass
class MemorySummary:
    summary_text: str
    source_reflections: list
    timestamp: datetime    

@dataclass
class CoachingContext:
    user_id: str
    current_reflection: Reflection
    recent_reflections: list[Reflection] 
    relevant_reflections: list
    memory_summary_current: MemorySummary | None
    memory_summary_history: list[MemorySummary]    

@dataclass
class CoachingResponse:
    message: str # primary coaching response
    follow_up_questions: list[str] # To drive engagement
    referenced_memories: list[str] # Explainability
    confidence: float | None = None # Future scoring/ranking
    model_info: dict | None = None  #Model name, tokens etc

