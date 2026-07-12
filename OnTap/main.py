from fastapi import FastAPI
from app.routers.vehicle_router import vehicle_router

app = FastAPI(title="Duong Dai Vehicle API")

app.include_router(vehicle_router)
