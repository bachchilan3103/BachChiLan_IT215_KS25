from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import SmartHomePlan
from ..schemas import SmartHomePlanCreate, SmartHomePlanResponse
from ..utils import standard_response

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/smart-home-plans")
def create_plan(payload: SmartHomePlanCreate, db: Session = Depends(get_db)):
    new_plan = SmartHomePlan(**payload.dict())
    try:
        db.add(new_plan)
        db.commit()
        db.refresh(new_plan)
        return standard_response(201, "Thêm gói thiết bị thành công", None,
                                 SmartHomePlanResponse.from_orm(new_plan).dict(),
                                 "/smart-home-plans")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,
                            detail=standard_response(400, "Plan code already exists", "Bad Request", None,
                                                     "/smart-home-plans"))

@router.get("/smart-home-plans")
def list_plans(db: Session = Depends(get_db)):
    plans = db.query(SmartHomePlan).all()
    return standard_response(200, "Lấy danh sách thành công", None,
                             [SmartHomePlanResponse.from_orm(p).dict() for p in plans],
                             "/smart-home-plans")

@router.get("/smart-home-plans/{plan_id}")
def get_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(SmartHomePlan).filter(SmartHomePlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404,
                            detail=standard_response(404, "Plan not found", "Not Found", None,
                                                     f"/smart-home-plans/{plan_id}"))
    return standard_response(200, "Chi tiết gói thiết bị", None,
                             SmartHomePlanResponse.from_orm(plan).dict(),
                             f"/smart-home-plans/{plan_id}")
