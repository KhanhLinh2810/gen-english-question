from pydantic import BaseModel
from typing import Optional

class ModelInput(BaseModel):
    """General request model structure for flutter incoming req."""
    user_id: Optional[str] = None
    context: str
    name: str

class ICQuestion(BaseModel):
    context: str
    name: str