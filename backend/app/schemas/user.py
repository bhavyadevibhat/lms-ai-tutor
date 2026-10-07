from typing import Literal
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class UserCreate(BaseModel):
    email: str
    username: str
    full_name: str
    password: str = Field(min_length=8, max_length=72)
    role: Literal["student", "instructor"] = "student"

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    username: str
    full_name: str
    role: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
