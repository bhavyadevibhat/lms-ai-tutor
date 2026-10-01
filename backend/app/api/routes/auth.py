from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.models import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth import hash_password, verify_password, create_access_token, verify_token, get_user_by_id
from fastapi.security import HTTPBearer, HTTPAuthCredentials

router = APIRouter(prefix="/api/auth", tags=["auth"])
security = HTTPBearer()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        password_hash=hash_password(user.password),
        role="student"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_login.email).first()
    if not db_user or not verify_password(user_login.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": db_user.id})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_me(credentials: HTTPAuthCredentials = Depends(security), db: Session = Depends(get_db)):
    user_id = verify_token(credentials.credentials)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
