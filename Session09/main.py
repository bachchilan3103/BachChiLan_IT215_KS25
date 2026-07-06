from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Any, Tuple
from datetime import datetime

tasks_db = [
    {
        "id": 1,
        "title": "Thiet ke database Shop AI",
        "description": "Xay dung bang va toi uu index",
        "assignee": "QuyDev",
        "priority": 1,
        "status": "todo",
        "created_at": "2026-07-01T09:00:00Z"
    },
    {
        "id": 2,
        "title": "Code bo API Authen",
        "description": "Trien khai filter verify JWT token",
        "assignee": "FixerQ",
        "priority": 2,
        "status": "done",
        "created_at": "2026-07-01T10:00:00Z"
    }
]

app = FastAPI()

class TaskBaseSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=1)
    assignee: str = Field(..., min_length=1)
    priority: int = Field(..., ge=1, le=5)

class TaskCreateSchema(TaskBaseSchema):
    pass

class TaskStatusUpdateSchema(BaseModel):
    status: str = Field(..., min_length=3)

def envelope(status_code: int, message: str, data: Any, error: Optional[str], path: str):
    return {
        "statusCode": status_code,
        "message": message,
        "data": data,
        "error": error,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "path": path
    }

@app.get("/tasks")
def get_all_tasks(status: Optional[str] = None):
    if status:
        filtered = [task for task in tasks_db if task["status"] == status]
        return envelope(200, "Lấy danh sách công việc thành công", filtered, None, "/tasks")
    return envelope(200, "Lấy danh sách công việc thành công", tasks_db, None, "/tasks")

@app.post("/tasks")
def create_task(task_in: TaskCreateSchema):
    for task in tasks_db:
        if task["title"].lower() == task_in.title.lower():
            raise HTTPException(
                status_code=400,
                detail=envelope(
                    400,
                    "Lỗi: Tiêu đề công việc này đã tồn tại trong nhóm",
                    None,
                    "ERR-TASK-01: Task conflict: Title field duplicates an existing record",
                    "/tasks"
                )
            )
    new_id = max([task["id"] for task in tasks_db], default=0) + 1
    new_task = {
        "id": new_id,
        "title": task_in.title,
        "description": task_in.description,
        "assignee": task_in.assignee,
        "priority": task_in.priority,
        "status": "todo",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    tasks_db.append(new_task)
    return envelope(201, "Khởi tạo công việc mới thành công", new_task, None, "/tasks")

@app.put("/tasks/{task_id}")
def update_task_status(task_id: int, status_in: TaskStatusUpdateSchema):
    for task in tasks_db:
        if task["id"] == task_id:
            if task["status"] == "done":
                raise HTTPException(
                    status_code=400,
                    detail=envelope(
                        400,
                        "Lỗi: Không thể cập nhật trạng thái công việc đã hoàn thành",
                        None,
                        "ERR-TASK-04: Task already completed, cannot update",
                        f"/tasks/{task_id}"
                    )
                )
            task["status"] = status_in.status
            return envelope(200, "Cập nhật tiến độ công việc thành công", task, None, f"/tasks/{task_id}")
    raise HTTPException(
        status_code=404,
        detail=envelope(
            404,
            "Lỗi: Không tìm thấy công việc với id này",
            None,
            "ERR-TASK-03: Task not found",
            f"/tasks/{task_id}"
        )
    )

def calculate_team_metrics() -> Tuple[int, int, float]:
    total = len(tasks_db)
    completed = sum(1 for task in tasks_db if task["status"] == "done")
    rate = (completed / total * 100) if total > 0 else 0.0
    return total, completed, rate

@app.get("/tasks/analytics/dashboard")
def get_dashboard_analytics():
    total, completed, rate = calculate_team_metrics()
    data = {
        "total_tasks": total,
        "completed_tasks": completed,
        "completion_rate_percentage": rate
    }
    return envelope(200, "Lấy số liệu thống kê hiệu suất nhóm thành công", data, None, "/tasks/analytics/dashboard")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=envelope(
            500,
            "Lỗi hệ thống nội bộ, vui lòng thử lại sau",
            None,
            "ERR-500: Internal Server Error",
            str(request.url.path)
        )
    )
