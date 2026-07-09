from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, BoardingSlot
from schemas import BoardingSlotCreate, BoardingSlotUpdate, BoardingSlotResponse
from datetime import datetime

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def build_response(status_code: int, message: str, error: str, data: dict, path: str):
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@app.post("/boarding-slots")
def create_slot(slot: BoardingSlotCreate, request: Request, db: Session = Depends(get_db)):
    try:
        if db.query(BoardingSlot).filter(BoardingSlot.slot_number == slot.slot_number).first():
            return build_response(400, "Slot number already exists", "Bad Request", None, str(request.url))
        new_slot = BoardingSlot(**slot.dict())
        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)
        return build_response(201, "Thêm khoang lưu trú thành công", None, BoardingSlotResponse.model_validate(new_slot).dict(), str(request.url))
    except Exception as e:
        db.rollback()
        return build_response(500, "Internal Server Error", str(e), None, str(request.url))

@app.get("/boarding-slots")
def get_slots(request: Request, db: Session = Depends(get_db)):
    slots = db.query(BoardingSlot).all()
    data = [BoardingSlotResponse.model_validate(s).dict() for s in slots]
    return build_response(200, "Lấy danh sách thành công", None, data, str(request.url))

@app.get("/boarding-slots/{slot_id}")
def get_slot(slot_id: int, request: Request, db: Session = Depends(get_db)):
    slot = db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()
    if not slot:
        return build_response(404, "Boarding slot not found", "Not Found", None, str(request.url))
    return build_response(200, "Chi tiết khoang lưu trú", None, BoardingSlotResponse.model_validate(slot).dict(), str(request.url))

@app.put("/boarding-slots/{slot_id}")
def update_slot(slot_id: int, slot: BoardingSlotUpdate, request: Request, db: Session = Depends(get_db)):
    try:
        db_slot = db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()
        if not db_slot:
            return build_response(404, "Boarding slot not found", "Not Found", None, str(request.url))
        update_data = slot.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_slot, key, value)
        db.commit()
        db.refresh(db_slot)
        return build_response(200, "Cập nhật khoang lưu trú thành công", None, BoardingSlotResponse.model_validate(db_slot).dict(), str(request.url))
    except Exception as e:
        db.rollback()
        return build_response(500, "Internal Server Error", str(e), None, str(request.url))

@app.delete("/boarding-slots/{slot_id}")
def delete_slot(slot_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        db_slot = db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()
        if not db_slot:
            return build_response(404, "Boarding slot not found", "Not Found", None, str(request.url))
        db.delete(db_slot)
        db.commit()
        return build_response(200, "Xóa khoang lưu trú thành công", None, None, str(request.url))
    except Exception as e:
        db.rollback()
        return build_response(500, "Internal Server Error", str(e), None, str(request.url))
