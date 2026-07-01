from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

students = [
    {"id": 1, "name": "Nguyen Van A"},
    {"id": 2, "name": "Tran Thi B"},
    {"id": 3, "name": "Le Van C"}
]

courses = [
    {"id": 1, "name": "FastAPI Basic", "capacity": 2},
    {"id": 2, "name": "Python OOP", "capacity": 2}
]

registrations = [
    {"id": 1, "student_id": 1, "course_id": 1},
    {"id": 2, "student_id": 2, "course_id": 1}
]

class RegistrationCreate(BaseModel):
    student_id: int
    course_id: int

@app.post("/registrations", status_code=201)
def create_registration(reg: RegistrationCreate):
    if not any(s["id"] == reg.student_id for s in students):
        raise HTTPException(status_code=400, detail="Student not found")
    
    course = next((c for c in courses if c["id"] == reg.course_id), None)
    if not course:
        raise HTTPException(status_code=400, detail="Course not found")
    
    for r in registrations:
        if r["student_id"] == reg.student_id and r["course_id"] == reg.course_id:
            raise HTTPException(status_code=400, detail="Student already registered this course")
    
    current_count = sum(1 for r in registrations if r["course_id"] == reg.course_id)
    if current_count >= course["capacity"]:
        raise HTTPException(status_code=400, detail="Course is full")
    
    new_id = max(r["id"] for r in registrations) + 1 if registrations else 1
    
    new_registration = {
        "id": new_id,
        "student_id": reg.student_id,
        "course_id": reg.course_id
    }
    registrations.append(new_registration)
    return new_registration
