# what the client is allowed to send 
from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_id: str
    role: str
    query: str


