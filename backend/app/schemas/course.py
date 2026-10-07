from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CourseCreate(BaseModel):
    title: str
    description: str
    category: str
    level: str = "beginner"
    price: float = 0

class CourseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    instructor_id: str
    title: str
    description: str
    category: str
    level: str
    price: float
    created_at: datetime
