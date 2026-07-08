from fastapi import FastAPI
from .routers import parking_slots
from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(parking_slots.router)
