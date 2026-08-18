from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

# =========================
# CORS
# =========================

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# =========================
# Fake database
# =========================

TOKENS = {
    "admin-token": {
        "username": "admin01",
        "role": "admin",
        "is_active": True,
    },
    "user-token": {
        "username": "student01",
        "role": "user",
        "is_active": True,
    },
    "locked-token": {
        "username": "locked01",
        "role": "user",
        "is_active": False,
    },
}


# =========================
# Middleware
# =========================

@app.middleware("http")
async def authentication_middleware(request: Request, call_next):

    # /health được truy cập công khai
    if request.url.path == "/health":
        response = await call_next(request)
        response.headers["X-System-Name"] = (
            "Learning Management System"
        )
        return response

    # CORS preflight không yêu cầu JWT
    if request.method == "OPTIONS":
        response = await call_next(request)
        response.headers["X-System-Name"] = (
            "Learning Management System"
        )
        return response

    # Các API còn lại phải có Authorization
    if "authorization" not in request.headers:
        return JSONResponse(
            status_code=401,
            content={
                "detail": "Authorization header is required"
            },
        )

    response = await call_next(request)

    response.headers["X-System-Name"] = (
        "Learning Management System"
    )

    return response


# =========================
# Authentication
# =========================

def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    user = TOKENS.get(token)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    if not user["is_active"]:
        raise HTTPException(
            status_code=401,
            detail="User account is inactive",
        )

    return user


# =========================
# Authorization - Admin
# =========================

def require_admin(
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin permission required",
        )

    return current_user


# =========================
# Public API
# =========================

@app.get("/health")
def health_check():
    return {"status": "UP"}


# =========================
# Protected API
# =========================

@app.get("/courses")
def get_courses(
    current_user: dict = Depends(get_current_user)
):
    return {
        "items": [
            {
                "id": 1,
                "name": "FastAPI Basic"
            },
            {
                "id": 2,
                "name": "FastAPI Security"
            },
        ]
    }


# =========================
# Admin API
# =========================

@app.delete("/admin/courses/{course_id}")
def delete_course(
    course_id: int,
    current_user: dict = Depends(require_admin),
):
    return {
        "message": f"Course {course_id} has been deleted",
        "deleted_by": current_user["username"],
    }