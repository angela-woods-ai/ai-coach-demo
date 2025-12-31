# Test the refactor
from dataclasses import asdict
import json

from .state import init_user_memory, clear_user_state
from .coach_engine import process_reflection
from .serializers import serialize_process_reflection_result

# Run from the terminal:  python -m ai.test_driver
if __name__ == "__main__":
    user_id = "user_123"

    init_user_memory(user_id)
    clear_user_state(user_id)

    # Some placeholder reflection history
    reflection_texts = [
        # Simple test sequence
        # Shift over time
        # First memory window: deadlines
        # "Work deadlines are exhausting",
        # "I feel stressed about work deadlines",
        # "Work has been overwhelming lately",
        # # #Second memory window: summary learning
        # "I feel more confident learning new skills", 
        # "Learning new things feels exciting",
        # "I enjoy learning and growing",
        # # # Third memory window: stress
        # "I felt stressed today"

        # More complex test sequence
        "Work deadlines have been overwhelming lately.", # Memory starts empty, introduce a theme: work + stress
        "Deadlines make it hard for me to relax, even after hours.", # Topic continuity across language variation
        "I've been enjoying learning new technical skills.", # Introduce a new theme - learning, branching happens, everything isn't collapsed into one them
        "Even though work is stressful, learning helps me feel grounded.", # Bridge themes: work stress + learning and the LLM can reason over both
        "What do I seem to come back to most?" # Meta reflection: learning as regulation on stress + deadlines
    ]

    for idx, text in enumerate(reflection_texts, start=1):
        result = process_reflection(user_id, idx, text)
        serialized_result = serialize_process_reflection_result(result)
    #    print(json.dumps(asdict(serialized_result), indent=2))
    
        # If I want to see relevent reflections for the current one
        print("Relevant Reflections:")
        for r in result.context.relevant_reflections:
            print("-", r.text)

        if(result.memory_updated):
            print(f"Memory Summary: {result.context.memory_summary_current.summary_text}")
        
        print(f"\n[Coach Response] {result.response.message} {result.response.follow_up_questions}\n")

    # # Test clearing the user
    # print("Clearing user")
    # clear_user_state(user_id)

    # # Some placeholder reflection history
    # reflection_texts_testclear = [
    #     "Today I was stressed.",
    #     "I am more stressed when I'm hungry.",
    #     "It is hard to sleep when I'm stressed.",
    # ]

    # for idx, text in enumerate(reflection_texts_testclear, start=1):
    #     result = process_reflection(user_id, idx, text)
    #     serialized_result = serialize_process_reflection_result(result)
    #     # print(json.dumps(asdict(serialized_result), indent=2))
    
    #     # If I want to see relevent reflections for the current one
    #     print("Relevant Reflections:")
    #     for r in result.context.relevant_reflections:
    #         print("-", r.text)

    #     print(f"\n[Coach Response] {result.response.message} {result.response.follow_up_questions}\n")