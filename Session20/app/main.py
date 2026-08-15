from fastapi import FastAPI

from database import engine, Base
from routes.students import router as student_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Management API"
)

app.include_router(student_router)


@app.get("/")
def root():
    return {
        "message": "Student Management API is running"
    }