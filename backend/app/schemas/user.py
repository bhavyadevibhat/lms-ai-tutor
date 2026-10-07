from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    username: str
    full_name: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    full_name: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
