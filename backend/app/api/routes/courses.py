from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.models import Course, User, Enrollment
from app.schemas.course import CourseCreate, CourseResponse
from app.services.auth import verify_token, get_user_by_id
from fastapi.security import HTTPBearer, HTTPAuthCredentials

router = APIRouter(prefix="/api/courses", tags=["courses"])
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthCredentials = Depends(security), db: Session = Depends(get_db)):
    user_id = verify_token(credentials.credentials)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    return get_user_by_id(db, user_id)

@router.post("/", response_model=CourseResponse)
def create_course(course: CourseCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "instructor":
        raise HTTPException(status_code=403, detail="Only instructors can create courses")
    
    db_course = Course(**course.dict(), instructor_id=current_user.id)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/")
def list_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: str, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.post("/{course_id}/enroll")
def enroll_course(course_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    existing = db.query(Enrollment).filter(
        Enrollment.student_id == current_user.id,
        Enrollment.course_id == course_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled")
    
    enrollment = Enrollment(student_id=current_user.id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    return {"message": "Successfully enrolled"}
