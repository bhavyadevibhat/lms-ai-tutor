from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import create_tables
from app.api.routes import auth, courses

app = FastAPI(
    title="LMS API",
    description="AI-Powered Learning Management System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    create_tables()
    print("✅ App started! Database initialized.")

app.include_router(auth.router)
app.include_router(courses.router)

@app.get("/")
def read_root():
    return {"message": "LMS API running!", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}
