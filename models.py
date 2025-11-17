from pydantic import BaseModel  # type: ignore

class ChatRequest(BaseModel):
    session_id: str
    query: str 
