from fastapi import FastAPI
from .routers.health import health

app = FastAPI()

app.include_router(health)
