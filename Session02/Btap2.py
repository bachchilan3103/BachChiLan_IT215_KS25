# Endpoint là đchỉ URL mà client gọi để truy cập vào 1 chức năng cụ thể của api
# Vì định nghĩa hàm dsach là students mà /student thì kco cho nên endpoint k thể tìm thấy
# vì /student là số ít chỉ biểu diễn dc 1 sviên, ycau đề bài thì theo qtac restful endpoint cho dsach nay phai la /students số nhiều
# students[0] chỉ trả về sviên đầu tiên của dsach chứ kphai tất cả 
# Get /students

from fastapi import FastAPI

app = FastAPI()
students = [{"id": 1, "name": "An"},
            {"id": 2, "name": "Binh"},
            {"id": 3, "name": "Cuong"},]

@app.get("/students")
def get_student():
    return {"students": students}