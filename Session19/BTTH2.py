from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
from pydantic import BaseModel
from typing import List, Optional

DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/health_system"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Clinic(Base):
    __tablename__ = "clinics"
    id = Column(Integer, primary_key=True, index=True)
    clinic_name = Column(String(255), nullable=False)
    specialty = Column(String(255), nullable=False)

    doctors = relationship("Doctor", back_populates="clinic")

class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    doctor_code = Column(String(255), nullable=False, unique=True)
    salary = Column(Float, nullable=False)
    clinic_id = Column(Integer, ForeignKey("clinics.id"), nullable=False)

    clinic = relationship("Clinic", back_populates="doctors")
    license = relationship("License", back_populates="doctor", uselist=False)

class License(Base):
    __tablename__ = "licenses"
    id = Column(Integer, primary_key=True, index=True)
    license_number = Column(String(255), nullable=False, unique=True)
    issue_by = Column(String(255), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), unique=True, nullable=False)

    doctor = relationship("Doctor", back_populates="license")

class LicenseResponse(BaseModel):
    id: int
    license_number: str
    issue_by: str
    class Config: from_attributes = True

class DoctorUpdate(BaseModel):
    doctor_code: Optional[str] = None
    salary: Optional[float] = None

class DoctorResponse(BaseModel):
    id: int
    doctor_code: str
    salary: float
    license: Optional[LicenseResponse]
    class Config: from_attributes = True

class ClinicCreate(BaseModel):
    clinic_name: str
    specialty: str

class ClinicDetailResponse(BaseModel):
    id: int
    clinic_name: str
    specialty: str
    doctors: List[DoctorResponse]
    class Config: from_attributes = True

app = FastAPI()

@app.post("/clinics", response_model=ClinicDetailResponse, status_code=201)
def create_clinic(clinic: ClinicCreate, db: Session = Depends(get_db)):
    new_clinic = Clinic(**clinic.dict())
    try:
        db.add(new_clinic)
        db.commit()
        db.refresh(new_clinic)
        return new_clinic
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating clinic")

@app.get("/clinics/{clinic_id}", response_model=ClinicDetailResponse)
def get_clinic_detail(clinic_id: int, db: Session = Depends(get_db)):
    cl = db.query(Clinic).filter(Clinic.id == clinic_id).first()
    if not cl:
        raise HTTPException(status_code=404, detail="Clinic not found")
    return cl

@app.patch("/doctors/{doctor_id}", response_model=DoctorResponse)
def update_doctor(doctor_id: int, doctor_update: DoctorUpdate, db: Session = Depends(get_db)):
    doc = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")

    update_data = doctor_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(doc, key, value)

    try:
        db.commit()
        db.refresh(doc)
        return doc
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating doctor")

@app.delete("/licenses/{license_id}")
def delete_license(license_id: int, db: Session = Depends(get_db)):
    lic = db.query(License).filter(License.id == license_id).first()
    if not lic:
        raise HTTPException(status_code=404, detail="License not found")

    try:
        db.delete(lic)
        db.commit()
        return {"detail": "License deleted successfully"}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting license")
