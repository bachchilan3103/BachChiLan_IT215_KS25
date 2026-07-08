from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import ParkingSlot
from ..schemas import ParkingSlotCreate, ParkingSlotResponse
from ..utils import standard_response

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/parking-slots")
def create_parking_slot(payload: ParkingSlotCreate, db: Session = Depends(get_db)):
    new_slot = ParkingSlot(**payload.dict())
    try:
        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)
        return standard_response(201, "Thêm vị trí đỗ xe thành công", None,
                                 ParkingSlotResponse.from_orm(new_slot).dict(),
                                 "/parking-slots")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/parking-slots")
def list_parking_slots(db: Session = Depends(get_db)):
    slots = db.query(ParkingSlot).all()
    return standard_response(200, "Danh sách vị trí đỗ xe", None,
                             [ParkingSlotResponse.from_orm(s).dict() for s in slots],
                             "/parking-slots")

@router.get("/parking-slots/{slot_id}")
def get_parking_slot(slot_id: int, db: Session = Depends(get_db)):
    slot = db.query(ParkingSlot).filter(ParkingSlot.id == slot_id).first()
    if not slot:
        raise HTTPException(status_code=404,
                            detail=standard_response(404, "Parking slot not found", "Not Found", None,
                                                     f"/parking-slots/{slot_id}"))
    return standard_response(200, "Chi tiết vị trí đỗ xe", None,
                             ParkingSlotResponse.from_orm(slot).dict(),
                             f"/parking-slots/{slot_id}")
