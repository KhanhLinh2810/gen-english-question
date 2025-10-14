from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional

class ICreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str

class IUpdateUser(BaseModel):
    username: str
    email: EmailStr
    password: Optional[str]

class IFilterUser(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    username_or_email: Optional[str] = None
