from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

courses = [
    {"id": 1, "code": "PY101", "name": "Python Basic", "duration": 30, "fee": 3000000},
    {"id": 2, "code": "API101", "name": "FastAPI Basic", "duration": 24, "fee": 2500000},
    {"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]

class CourseRequest(BaseModel):
    code: str
    name: str
    duration: int
    fee: int

@app.get("/courses", tags=["Courses"], status_code=status.HTTP_200_OK)
def get_courses(keyword: Optional[str] = None, min_fee: Optional[int] = None, max_fee: Optional[int] = None):
    result = courses
    if keyword:
        result = [c for c in result if keyword.lower() in c["name"].lower() or keyword.lower() in c["code"].lower()]
    if min_fee is not None:
        result = [c for c in result if c["fee"] >= min_fee]
    if max_fee is not None:
        result = [c for c in result if c["fee"] <= max_fee]
    return {
        "status": "success",
        "message": "Lấy danh sách khóa học thành công",
        "data": result
    }

@app.get("/courses/{course_id}", tags=["Courses"])
def get_course_by_id(course_id: int):
    for course in courses:
        if course["id"] == course_id:
            return {
                "status": "success",
                "message": "Lấy khóa học thành công",
                "data": course
            }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy khóa học")

@app.post("/courses", tags=["Courses"], status_code=status.HTTP_201_CREATED)
def create_course(course: CourseRequest):
    if not course.name.strip():
        raise HTTPException(status_code=400, detail="Tên khóa học không được rỗng")
    if course.duration <= 0:
        raise HTTPException(status_code=400, detail="Thời lượng phải > 0")
    if course.fee < 0:
        raise HTTPException(status_code=400, detail="Học phí phải >= 0")
    for c in courses:
        if c["code"] == course.code:
            raise HTTPException(status_code=400, detail="Mã khóa học đã tồn tại")

    new_id = max(c["id"] for c in courses) + 1 if courses else 1
    new_course = {"id": new_id, **course.dict()}
    courses.append(new_course)
    return {
        "status": "success",
        "message": "Tạo mới khóa học thành công",
        "data": new_course
    }

@app.put("/courses/{course_id}", tags=["Courses"])
def update_course(course_id: int, course_receive: CourseRequest):
    for index, course in enumerate(courses):
        if course["id"] == course_id:
            for other in courses:
                if other["code"] == course_receive.code and other["id"] != course_id:
                    raise HTTPException(status_code=400, detail="Mã khóa học đã tồn tại")

            if not course_receive.name.strip():
                raise HTTPException(status_code=400, detail="Tên khóa học không được rỗng")
            if course_receive.duration <= 0:
                raise HTTPException(status_code=400, detail="Thời lượng phải > 0")
            if course_receive.fee < 0:
                raise HTTPException(status_code=400, detail="Học phí phải >= 0")

            courses[index].update(course_receive.dict())
            return {
                "status": "success",
                "message": "Cập nhật khóa học thành công",
                "data": courses[index]
            }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy khóa học")

@app.delete("/courses/{course_id}", tags=["Courses"])
def delete_course(course_id: int):
    for index, course in enumerate(courses):
        if course["id"] == course_id:
            del courses[index]
            return {
                "status": "success",
                "message": "Xóa khóa học thành công"
            }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy khóa học")
