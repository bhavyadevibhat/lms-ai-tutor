from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import create_tables
from app.api.routes import auth, courses

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(
    title="LMS API",
    description="AI-Powered Learning Management System",
    version="1.0.0",
    lifespan=lifespan,
)

# Open CORS is fine for development. Restrict origins before going live.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(courses.router)

@app.get("/")
def read_root():
    return {"message": "LMS API running!", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}
