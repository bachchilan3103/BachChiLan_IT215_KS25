from fastapi import FastAPI
from .database import Base, engine
from .routers import smart_home_plans

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(smart_home_plans.router)
