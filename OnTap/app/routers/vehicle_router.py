from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.services.vehicle_service import VehicleService
from app.schemas.vehicle_schema import VehicleCreate, VehicleUpdate
from app.database import get_db
from app.utils import format_response

vehicle_router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"]
)

@vehicle_router.get("/")
def get_all_vehicles(request: Request, brand: str = None, status: str = None,
                     sort_by: str = None, order: str = None, db: Session = Depends(get_db)):
    try:
        data = VehicleService.get_all(db, brand, status, sort_by, order)
        return format_response(200, data, "Fetched successfully", str(request.url))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@vehicle_router.get("/{vehicle_id}")
def get_vehicle(vehicle_id: str, request: Request, db: Session = Depends(get_db)):
    vehicle = VehicleService.get_by_id(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return format_response(200, vehicle, "Vehicle found", str(request.url))

@vehicle_router.post("/")
def create_vehicle(vehicle: VehicleCreate, request: Request, db: Session = Depends(get_db)):
    if VehicleService.get_by_id(db, vehicle.id):
        raise HTTPException(status_code=409, detail="Vehicle ID already exists")
    new_vehicle = VehicleService.create(db, vehicle)
    return format_response(201, new_vehicle, "Vehicle created successfully", str(request.url))

@vehicle_router.put("/{vehicle_id}")
def update_vehicle(vehicle_id: str, data: VehicleUpdate, request: Request, db: Session = Depends(get_db)):
    updated = VehicleService.update(db, vehicle_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return format_response(200, updated, "Vehicle updated successfully", str(request.url))

@vehicle_router.delete("/{vehicle_id}")
def delete_vehicle(vehicle_id: str, request: Request, db: Session = Depends(get_db)):
    deleted = VehicleService.delete(db, vehicle_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return format_response(200, None, "Vehicle deleted successfully", str(request.url))
