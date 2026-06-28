from fastapi import FastAPI

app = FastAPI()

students = [
    {"id": 1, "name": "An", "status": "active"},
    {"id": 2, "name": "Binh", "status": "inactive"},
    {"id": 3, "name": "Cuong", "status": "active"},
    {"id": 4, "name": "Dung", "status": "pending"}
]

@app.get("/students/active")
def get_active_students():
    active_students = [s for s in students if s["status"] == "active"]
    if not active_students:
        return {
            "message": "Kh có sinh viên đang học",
            "data": []}
    return {
        "message": "Danh sách sinh viên đang học",
        "data": active_students}
