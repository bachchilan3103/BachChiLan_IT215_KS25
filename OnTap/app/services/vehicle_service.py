from sqlalchemy.orm import Session
from app.models.vehicle_model import Vehicle
from app.schemas.vehicle_schema import VehicleCreate, VehicleUpdate

class VehicleService:
    @staticmethod
    def get_all(db: Session, brand=None, status=None, sort_by=None, order=None):
        query = db.query(Vehicle)
        if brand:
            query = query.filter(Vehicle.brand.ilike(f"%{brand}%"))
        if status:
            query = query.filter(Vehicle.status == status)
        if sort_by in ["daily_rate", "production_year"]:
            sort_column = getattr(Vehicle, sort_by)
            query = query.order_by(sort_column.desc() if order == "desc" else sort_column.asc())
        else:
            query = query.order_by(Vehicle.id.asc())
        return query.all()

    @staticmethod
    def get_by_id(db: Session, vehicle_id: str):
        return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    @staticmethod
    def create(db: Session, vehicle: VehicleCreate):
        db_vehicle = Vehicle(**vehicle.dict())
        db.add(db_vehicle)
        db.commit()
        db.refresh(db_vehicle)
        return db_vehicle

    @staticmethod
    def update(db: Session, vehicle_id: str, data: VehicleUpdate):
        db_vehicle = VehicleService.get_by_id(db, vehicle_id)
        if db_vehicle:
            for key, value in data.dict().items():
                setattr(db_vehicle, key, value)
            db.commit()
            db.refresh(db_vehicle)
        return db_vehicle

    @staticmethod
    def delete(db: Session, vehicle_id: str):
        db_vehicle = VehicleService.get_by_id(db, vehicle_id)
        if db_vehicle:
            db.delete(db_vehicle)
            db.commit()
        return db_vehicle
