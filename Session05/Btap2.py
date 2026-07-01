from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

enrollments = [
    {
        "id": 1,
        "student_id": "SV001",
        "course_id": 1
    },
    {
        "id": 2,
        "student_id": "SV002",
        "course_id": 1
    }
]

class EnrollmentCreate(BaseModel):
    student_id: str
    course_id: int

@app.post("/enrollments", status_code=201)
def create_enrollment(enrollment: EnrollmentCreate):
    for e in enrollments:
        if e["student_id"] == enrollment.student_id and e["course_id"] == enrollment.course_id:
            raise HTTPException(
                status_code=400,
                detail=f"Học viên {enrollment.student_id} đã đăng ký khóa học {enrollment.course_id}."
            )
    new_id = max(e["id"] for e in enrollments) + 1 if enrollments else 1
    
    new_enrollment = {
        "id": new_id,
        "student_id": enrollment.student_id,
        "course_id": enrollment.course_id
    }
    enrollments.append(new_enrollment)
    return new_enrollment
