from anthropic import Anthropic
import json
from .prompts import build_coaching_prompt
from ..models import CoachingContext, CoachingResponse
from ..config import ANTHROPIC_API_KEY, USE_CLAUDE

client = Anthropic(api_key=ANTHROPIC_API_KEY)
claude_model="claude-3-haiku-20240307" # cheapest + fast - cost is fractions of a cent per relection

def claude_coach(context: CoachingContext) -> CoachingResponse:

    # Guard against cost mistakes
    if not USE_CLAUDE:
        raise RuntimeError("Claude called while USE_CLAUDE=false")
      
    prompt = build_coaching_prompt(context)

    response = client.messages.create(
        model=claude_model,
        max_tokens=400,
        temperature=0.7,
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    raw = response.content[0].text

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError(f"Claude returned invalid JSON:\n{raw}")
    
    return CoachingResponse(
        message=data["message"],
        follow_up_questions=data.get("follow_up_questions", []),
        referenced_memories=data.get("referenced_memories", []),
        confidence=.9, # Mocked for now
        model_info = {
            "provider": "anthropic",
            "model": claude_model,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        }
    )

