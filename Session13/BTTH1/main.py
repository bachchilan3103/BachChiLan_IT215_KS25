from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, MenuItem
from schemas import MenuItemCreate, MenuItemUpdate, MenuItemResponse
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

@app.post("/menu-items")
def create_item(item: MenuItemCreate, request: Request, db: Session = Depends(get_db)):
    try:
        if db.query(MenuItem).filter(MenuItem.dish_code == item.dish_code).first():
            return build_response(400, "Dish code already exists", "Bad Request", None, str(request.url))
        new_item = MenuItem(**item.dict())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return build_response(201, "Thêm món ăn thành công", None, MenuItemResponse.model_validate(new_item).dict(), str(request.url))
    except Exception as e:
        db.rollback()
        return build_response(500, "Internal Server Error", str(e), None, str(request.url))

@app.get("/menu-items")
def get_items(request: Request, db: Session = Depends(get_db)):
    items = db.query(MenuItem).all()
    data = [MenuItemResponse.model_validate(i).dict() for i in items]
    return build_response(200, "Danh sách món ăn", None, data, str(request.url))

@app.get("/menu-items/{item_id}")
def get_item(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        return build_response(404, "Menu item not found", "Not Found", None, str(request.url))
    return build_response(200, "Chi tiết món ăn", None, MenuItemResponse.model_validate(item).dict(), str(request.url))

@app.put("/menu-items/{item_id}")
def update_item(item_id: int, item: MenuItemUpdate, request: Request, db: Session = Depends(get_db)):
    try:
        db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
        if not db_item:
            return build_response(404, "Menu item not found", "Not Found", None, str(request.url))
        update_data = item.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
        return build_response(200, "Cập nhật món ăn thành công", None, MenuItemResponse.model_validate(db_item).dict(), str(request.url))
    except Exception as e:
        db.rollback()
        return build_response(500, "Internal Server Error", str(e), None, str(request.url))

@app.delete("/menu-items/{item_id}")
def delete_item(item_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
        if not db_item:
            return build_response(404, "Menu item not found", "Not Found", None, str(request.url))
        db.delete(db_item)
        db.commit()
        return build_response(200, "Xóa món ăn thành công", None, None, str(request.url))
    except Exception as e:
        db.rollback()
        return build_response(500, "Internal Server Error", str(e), None, str(request.url))
