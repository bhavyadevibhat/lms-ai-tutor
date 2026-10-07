from sqlalchemy import Column, String, Integer, DateTime, Boolean, Float, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    full_name = Column(String)
    role = Column(String, default="student")
    created_at = Column(DateTime, default=datetime.utcnow)

    courses = relationship("Course", back_populates="instructor")
    enrollments = relationship("Enrollment", back_populates="student")

class Course(Base):
    __tablename__ = "courses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    instructor_id = Column(String, ForeignKey("users.id"))
    title = Column(String, index=True)
    description = Column(Text)
    category = Column(String)
    level = Column(String, default="beginner")
    price = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    instructor = relationship("User", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String, ForeignKey("users.id"))
    course_id = Column(String, ForeignKey("courses.id"))
    enrolled_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
