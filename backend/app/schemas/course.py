from pydantic import BaseModel
from datetime import datetime

class CourseCreate(BaseModel):
    title: str
    description: str
    category: str
    level: str = "beginner"
    price: float = 0

class CourseResponse(BaseModel):
    id: str
    instructor_id: str
    title: str
    description: str
    category: str
    level: str
    price: float
    created_at: datetime

    class Config:
        from_attributes = True
