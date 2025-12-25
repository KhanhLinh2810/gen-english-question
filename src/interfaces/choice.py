from pydantic import BaseModel
from typing import Optional

class IChoice(BaseModel):
    content: str
    is_correct: bool
    explanation: Optional[str] = None