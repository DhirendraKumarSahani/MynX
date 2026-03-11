from pydantic import BaseModel
from typing import List


class ChatGPTStyleResponse(BaseModel):
    """
    Structured response returned to API clients.
    """
    
    title: str
    definition: str
    key_points: List[str]
    summary: str
    references: List[str]