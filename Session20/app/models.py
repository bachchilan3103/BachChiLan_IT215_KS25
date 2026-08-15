from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Classroom(Base):
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True, index=True)
    class_code = Column(String(20), unique=True, nullable=False)
    class_name = Column(String(100), nullable=False)
    max_students = Column(Integer, nullable=False)
    status = Column(String(20), default="active")

    students = relationship(
        "Student",
        back_populates="classroom"
    )


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_code = Column(String(20), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)

    class_id = Column(
        Integer,
        ForeignKey("classrooms.id"),
        nullable=False
    )

    classroom = relationship(
        "Classroom",
        back_populates="students"
    )