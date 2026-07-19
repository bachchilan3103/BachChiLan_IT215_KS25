from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
from pydantic import BaseModel
from typing import List, Optional

DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/supply_chain"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Warehouse(Base):
    __tablename__ = "warehouses"
    id = Column(Integer, primary_key=True, index=True)
    warehouse_name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    packages = relationship("Package", back_populates="warehouse")

class Package(Base):
    __tablename__ = "packages"
    id = Column(Integer, primary_key=True, index=True)
    package_code = Column(String(255), nullable=False, unique=True)
    weight = Column(Float, nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)

    warehouse = relationship("Warehouse", back_populates="packages")
    waybill = relationship("Waybill", back_populates="package", uselist=False)

class Waybill(Base):
    __tablename__ = "waybills"
    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String(255), nullable=False, unique=True)
    shipping_status = Column(String(255), nullable=False)
    package_id = Column(Integer, ForeignKey("packages.id"), unique=True, nullable=False)

    package = relationship("Package", back_populates="waybill")

class WaybillResponse(BaseModel):
    id: int
    tracking_number: str
    shipping_status: str
    class Config: from_attributes = True

class PackageUpdate(BaseModel):
    package_code: Optional[str] = None
    weight: Optional[float] = None

class PackageResponse(BaseModel):
    id: int
    package_code: str
    weight: float
    waybill: Optional[WaybillResponse]
    class Config: from_attributes = True

class WarehouseCreate(BaseModel):
    warehouse_name: str
    location: str

class WarehouseDetailResponse(BaseModel):
    id: int
    warehouse_name: str
    location: str
    packages: List[PackageResponse]
    class Config: from_attributes = True

app = FastAPI()

@app.post("/warehouses", response_model=WarehouseDetailResponse, status_code=201)
def create_warehouse(warehouse: WarehouseCreate, db: Session = Depends(get_db)):
    new_wh = Warehouse(**warehouse.dict())
    try:
        db.add(new_wh)
        db.commit()
        db.refresh(new_wh)
        return new_wh
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating warehouse")

@app.get("/warehouses/{warehouse_id}", response_model=WarehouseDetailResponse)
def get_warehouse_detail(warehouse_id: int, db: Session = Depends(get_db)):
    wh = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not wh:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return wh

@app.patch("/packages/{package_id}", response_model=PackageResponse)
def update_package(package_id: int, package_update: PackageUpdate, db: Session = Depends(get_db)):
    pkg = db.query(Package).filter(Package.id == package_id).first()
    if not pkg:
        raise HTTPException(status_code=404, detail="Package not found")

    update_data = package_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(pkg, key, value)

    try:
        db.commit()
        db.refresh(pkg)
        return pkg
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating package")

@app.delete("/waybills/{waybill_id}")
def delete_waybill(waybill_id: int, db: Session = Depends(get_db)):
    wb = db.query(Waybill).filter(Waybill.id == waybill_id).first()
    if not wb:
        raise HTTPException(status_code=404, detail="Waybill not found")

    try:
        db.delete(wb)
        db.commit()
        return {"detail": "Waybill deleted successfully"}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting waybill")

