import json
from ..models import CoachingContext

# Turn the CoachingContext object into a Claude prompt
def build_coaching_prompt(context: CoachingContext) -> str:
    relevant = "\n".join(
        f"- {r.text}" for r in context.relevant_reflections
    ) if context.relevant_reflections else "None available"

    memory = (
        context.memory_summary_current.summary_text
        if context.memory_summary_current
        else "None available"
    )

    # Escape the user's reflection to prevent JSON issues
    escaped_reflection = json.dumps(context.current_reflection.text)

    return f"""You are a thoughtful, supportive AI coach. Be warm but concise. Focus on insight over length.

CRITICAL: Respond with ONLY valid JSON. No preamble, no markdown backticks, no explanations.

User's latest reflection:
{escaped_reflection}

Relevant past reflections:
{relevant}

Long-term memory summary:
{memory}

Respond with JSON in this exact shape:
{{
  "message": "2-3 empathetic sentences acknowledging their reflection and offering insight",
  "follow_up_questions": ["1-2 thoughtful questions that help them reflect deeper"],
  "referenced_memories": ["Specific past reflections you're connecting to, if any"]
}}

If you cannot respond helpfully, return:
{{"message": "I need more context to respond meaningfully.", "follow_up_questions": [], "referenced_memories": []}}
"""
