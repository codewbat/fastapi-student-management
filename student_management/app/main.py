from fastapi import FastAPI
from routes.StudentRoutes import student_routes
from fastapi.middleware.cors import CORSMiddleware
from core.config import Config
from core.postgressDatabase import init_db , check_connection

student_app = FastAPI()
student_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@student_app.on_event("startup")
async def startup():
    if Config.is_postgres():
        print("🔍 Checking PostgreSQL connection...")
        check_connection()
        print("📦 Creating tables...")
        init_db()
    else:
        print("✅ Using JSON storage")
    
student_app.include_router(student_routes)