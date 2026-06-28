# Đổi endpoint theo chuẩn restful /students thay vì /getStudents
# Trả về json array đúng chuẩn FastAPI
# Kh dùng str để nối dữ liệu

from fastapi import FastAPI

app = FastAPI()
students = ["An", "Binh", "Cuong"]

@app.get("/students")
def get_students():
    return {"students": students}
