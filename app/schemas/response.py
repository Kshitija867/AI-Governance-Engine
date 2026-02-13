# what your server promises to return 
from pydantic import BaseModel

class ChatResponse(BaseModel):
    user_id: str
    role: str
    query: str
    decision: str
    message: str