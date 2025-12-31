# Expose the Python AI layer as a service
# Use FastAPI for the HTTP & JSON in/out
# API calls call the python layer to perform core logic then convert the result into serialized json
# FastAPI runs on localhost:8000
# Swaggger can be accessed at http://127.0.0.1:8000/docs for making debug calls
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from .coach_engine import process_reflection
from .state import init_user_memory, clear_user_state
from .serializers import serialize_process_reflection_result

app = FastAPI(title="AI Coach API")

# ---- Simple in-memory user (prototype only) ----
USER_ID = "test_user"

init_user_memory(USER_ID)
clear_user_state(USER_ID)


# ---- Request / Response Models ----

class ReflectionRequest(BaseModel):
    idx: int
    text: str


class ClearMemoryResponse(BaseModel):
    status: str


# ---- Routes ----

@app.post("/process_reflection")
def process_reflection_api(req: ReflectionRequest):
    # Process the reflection into the domain object
    result = process_reflection(
        user_id=USER_ID,
        idx=req.idx,
        text=req.text
    )

    # Serialize it
    return serialize_process_reflection_result(result)


@app.post("/clear_memory", response_model=ClearMemoryResponse)
def clear_memory():
    clear_user_state(USER_ID)
    init_user_memory(USER_ID)
    return {"status": "cleared"}
