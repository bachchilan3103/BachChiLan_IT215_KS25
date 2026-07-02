from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class UserResponse(BaseModel):
    id: int
    username: str
    fullname: str

class BaseUserResponse(BaseModel):
    status: str
    message: str
    data: UserResponse

users = [
    {
        "id": 1,
        "username": "nguyenvana",
        "password": "Abcd@1234",
        "fullname": "Nguyễn Văn A",
        "visa": "012345678"
    },
    {
        "id": 2,
        "username": "nguyenvanb",
        "password": "Abcd@1234567",
        "fullname": "Nguyễn Văn B",
        "visa": "09876543"
    },
    {
        "id": 3,
        "username": "nguyenvanc",
        "password": "Abcd@1234asd",
        "fullname": "Nguyễn Văn C",
        "visa": "01478523"
    }
]

@app.get("/users/{user_id}", tags=["Users"], response_model=BaseUserResponse)
def get_user_by_id(user_id: int):
    for user in users:
        if user["id"] == user_id:
            # return user
            return {
                "status": "success",
                "message": "Lấy dữ liệu người dùng thành công",
                "data": user
            }

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy người dùng")