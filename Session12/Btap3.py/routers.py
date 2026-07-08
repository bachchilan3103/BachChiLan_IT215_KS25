from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import ShipmentUpdate
from ..services import update_shipment_service

router = APIRouter()

@router.put("/shipments/{shipment_id}")
def update_shipment(shipment_id: int, shipment_update: ShipmentUpdate, db: Session = Depends(get_db)):
    shipment = update_shipment_service(db, shipment_id, shipment_update)
    return {
        "message": "Shipment updated successfully",
        "data": {
            "id": shipment.id,
            "tracking_code": shipment.tracking_code,
            "receiver_name": shipment.receiver_name,
            "delivery_address": shipment.delivery_address
        }
    }
