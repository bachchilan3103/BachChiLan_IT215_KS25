from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from database import get_db
from models import Student, Classroom
from schemas import StudentCreate, StudentResponse

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.get("")
def get_students(
    search: str | None = None,
    class_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Student)

    if search:
        query = query.filter(
            (Student.full_name.ilike(f"%{search}%")) |
            (Student.student_code.ilike(f"%{search}%")) |
            (Student.email.ilike(f"%{search}%"))
        )

    if class_id:
        query = query.filter(Student.class_id == class_id)

    students = query.all()

    return {
        "statusCode": 200,
        "message": "Lấy danh sách sinh viên thành công",
        "data": students,
        "error": None,
        "timestamp": "2026-07-15T10:00:00Z",
        "path": "/students"
    }


@router.get("/{student_id}")
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sinh viên"
        )

    return {
        "statusCode": 200,
        "message": "Lấy thông tin sinh viên thành công",
        "data": student,
        "error": None,
        "timestamp": "2026-07-15T10:00:00Z",
        "path": f"/students/{student_id}"
    }


@router.post("", status_code=status.HTTP_201_CREATED)
def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db)
):
    classroom = db.query(Classroom).filter(
        Classroom.id == student_data.class_id
    ).first()

    if not classroom:
        raise HTTPException(
            status_code=404,
            detail="Lớp học không tồn tại"
        )

    if classroom.status != "active":
        raise HTTPException(
            status_code=400,
            detail="Lớp học không hoạt động"
        )

    current_count = db.query(Student).filter(
        Student.class_id == classroom.id
    ).count()

    if current_count >= classroom.max_students:
        raise HTTPException(
            status_code=400,
            detail="Lớp học đã đủ số lượng sinh viên"
        )

    if db.query(Student).filter(
        Student.student_code == student_data.student_code
    ).first():
        raise HTTPException(
            status_code=400,
            detail="Mã sinh viên đã tồn tại"
        )

    if db.query(Student).filter(
        Student.email == student_data.email
    ).first():
        raise HTTPException(
            status_code=400,
            detail="Email đã tồn tại"
        )

    student = Student(
        student_code=student_data.student_code,
        full_name=student_data.full_name,
        email=student_data.email,
        age=student_data.age,
        gender=student_data.gender,
        class_id=student_data.class_id
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return {
        "statusCode": 201,
        "message": "Thêm sinh viên thành công",
        "data": student,
        "error": None,
        "timestamp": "2026-07-15T10:00:00Z",
        "path": "/students"
    }


@router.put("/{student_id}")
def update_student(
    student_id: int,
    student_data: StudentCreate,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sinh viên"
        )

    duplicate_code = db.query(Student).filter(
        Student.student_code == student_data.student_code,
        Student.id != student_id
    ).first()

    if duplicate_code:
        raise HTTPException(
            status_code=400,
            detail="Mã sinh viên đã tồn tại"
        )

    duplicate_email = db.query(Student).filter(
        Student.email == student_data.email,
        Student.id != student_id
    ).first()

    if duplicate_email:
        raise HTTPException(
            status_code=400,
            detail="Email đã tồn tại"
        )

    if student.class_id != student_data.class_id:

        classroom = db.query(Classroom).filter(
            Classroom.id == student_data.class_id
        ).first()

        if not classroom:
            raise HTTPException(
                status_code=404,
                detail="Lớp học không tồn tại"
            )

        if classroom.status != "active":
            raise HTTPException(
                status_code=400,
                detail="Lớp học không hoạt động"
            )

        current_count = db.query(Student).filter(
            Student.class_id == classroom.id
        ).count()

        if current_count >= classroom.max_students:
            raise HTTPException(
                status_code=400,
                detail="Lớp học đã đủ số lượng sinh viên"
            )

    student.student_code = student_data.student_code
    student.full_name = student_data.full_name
    student.email = student_data.email
    student.age = student_data.age
    student.gender = student_data.gender
    student.class_id = student_data.class_id

    db.commit()
    db.refresh(student)

    return {
        "statusCode": 200,
        "message": "Cập nhật sinh viên thành công",
        "data": student,
        "error": None,
        "timestamp": "2026-07-15T10:00:00Z",
        "path": f"/students/{student_id}"
    }