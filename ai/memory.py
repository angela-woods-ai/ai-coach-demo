# Memory & Summarization logic

from datetime import datetime
from .state import USER_MEMORY_SUMMARIES
from .models import MemorySummary
from collections import Counter

# Simple summarizer: crude & deterministic - later Claude can gnerate MemorySummary and use it as compressed context and Help update it incrementally
# keeps words that: appear ≥ 2 times are longer than 4 characters
def summarize_reflections(reflections: list) -> MemorySummary:
    if not reflections:
        return None

    combined_text = " ".join(r.text for r in reflections)
    words = combined_text.lower().split()

    common_words = [
        word for word, count in Counter(words).items()
        if count >= 2 and len(word) > 4
    ]

    summary = (
        "You often mention: "
        + ", ".join(common_words[:5])
        if common_words
        else "No strong recurring themes yet."
    )

    return MemorySummary(
        summary_text=summary,
        source_reflections=reflections,
        timestamp=datetime.now()
    )

