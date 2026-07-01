from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, EmailStr
from typing import Optional

app = FastAPI()

students = [
    {"id": 1, "code": "SV001", "name": "Nguyen Van A", "email": "a@gmail.com", "age": 20},
    {"id": 2, "code": "SV002", "name": "Tran Thi B", "email": "b@gmail.com", "age": 22},
    {"id": 3, "code": "SV003", "name": "Le Van C", "email": "c@gmail.com", "age": 21}
]

class StudentRequest(BaseModel):
    code: str
    name: str
    email: EmailStr
    age: int

@app.get("/students", tags=["Students"], status_code=status.HTTP_200_OK)
def get_students(keyword: Optional[str] = None, min_age: Optional[int] = None, max_age: Optional[int] = None):
    result = students
    if keyword:
        result = [s for s in result if keyword.lower() in s["name"].lower() or keyword.lower() in s["email"].lower()]
    if min_age is not None:
        result = [s for s in result if s["age"] >= min_age]
    if max_age is not None:
        result = [s for s in result if s["age"] <= max_age]
    return {
        "status": "success",
        "message": "Lấy danh sách học viên thành công",
        "data": result
    }

@app.get("/students/{student_id}", tags=["Students"])
def get_student_by_id(student_id: int):
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Không tìm thấy học viên")
    return {
        "status": "success",
        "message": "Lấy học viên thành công",
        "data": student
    }

@app.post("/students", tags=["Students"], status_code=status.HTTP_201_CREATED)
def create_student(student: StudentRequest):
    for s in students:
        if s["code"] == student.code:
            raise HTTPException(status_code=400, detail="Mã học viên đã tồn tại")
        if s["email"] == student.email:
            raise HTTPException(status_code=400, detail="Email đã tồn tại")

    new_id = max(s["id"] for s in students) + 1 if students else 1
    new_student = {"id": new_id, **student.dict()}
    students.append(new_student)
    return {
        "status": "success",
        "message": "Tạo mới học viên thành công",
        "data": new_student
    }

@app.put("/students/{student_id}", tags=["Students"])
def update_student(student_id: int, student_receive: StudentRequest):
    for index, s in enumerate(students):
        if s["id"] == student_id:
            for other in students:
                if other["id"] != student_id and (other["code"] == student_receive.code or other["email"] == student_receive.email):
                    raise HTTPException(status_code=400, detail="Code hoặc Email đã tồn tại")

            students[index].update(student_receive.dict())
            return {
                "status": "success",
                "message": "Cập nhật học viên thành công",
                "data": students[index]
            }
    raise HTTPException(status_code=404, detail="Không tìm thấy học viên")

@app.delete("/students/{student_id}", tags=["Students"])
def delete_student(student_id: int):
    for index, s in enumerate(students):
        if s["id"] == student_id:
            del students[index]
            return {
                "status": "success",
                "message": "Xóa học viên thành công"
            }
    raise HTTPException(status_code=404, detail="Không tìm thấy học viên")
