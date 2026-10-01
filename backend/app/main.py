from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import create_tables
from app.api.routes import auth, courses

app = FastAPI(title="LMS API", version="1.0.0")

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
    print("✅ App started!")

app.include_router(auth.router)
app.include_router(courses.router)

@app.get("/")
def root():
    return {"message": "LMS API running!"}

@app.get("/health")
def health():
    return {"status": "healthy"}
