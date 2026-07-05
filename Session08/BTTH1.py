from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

class Carrier(BaseModel):
    id: int
    code: str
    name: str = Field(..., min_length=3)
    max_weight_capacity: int = Field(..., gt=0)
    status: str

class CarrierCreate(BaseModel):
    code: str
    name: str = Field(..., min_length=3)
    max_weight_capacity: int = Field(..., gt=0)
    status: str

class Shipment(BaseModel):
    id: int
    carrier_id: int
    order_reference: str
    total_weight: int = Field(..., gt=0)
    dispatch_date: str
    shift: str

class ShipmentCreate(BaseModel):
    carrier_id: int
    order_reference: str
    total_weight: int = Field(..., gt=0)
    dispatch_date: str
    shift: str

carriers: List[Carrier] = [
    Carrier(id=1, code="GHN", name="Giao Hang Nhanh", max_weight_capacity=5000, status="ACTIVE"),
    Carrier(id=2, code="GHTK", name="Giao Hang Tiet Kiem", max_weight_capacity=3000, status="ACTIVE"),
    Carrier(id=3, code="VTP", name="Viettel Post", max_weight_capacity=10000, status="SUSPENDED"),
]

shipments: List[Shipment] = [
    Shipment(id=1, carrier_id=1, order_reference="ORD-2026-001", total_weight=4200,
             dispatch_date="2026-07-01", shift="MORNING")
]

valid_statuses = {"ACTIVE", "INACTIVE", "SUSPENDED"}
valid_shifts = {"MORNING", "AFTERNOON", "NIGHT"}

@app.post("/carriers", response_model=Carrier)
def create_carrier(carrier: CarrierCreate):
    if any(c.code == carrier.code for c in carriers):
        raise HTTPException(status_code=400, detail="Carrier code must be unique")
    if carrier.status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
    new_carrier = Carrier(id=len(carriers) + 1, **carrier.dict())
    carriers.append(new_carrier)
    return new_carrier

@app.get("/carriers", response_model=List[Carrier])
def list_carriers(keyword: Optional[str] = None,
                  status: Optional[str] = None,
                  min_weight: Optional[int] = None):
    result = carriers
    if keyword:
        kw = keyword.lower()
        result = [c for c in result if kw in c.code.lower() or kw in c.name.lower()]
    if status:
        result = [c for c in result if c.status == status]
    if min_weight:
        result = [c for c in result if c.max_weight_capacity >= min_weight]
    return result

@app.get("/carriers/{carrier_id}", response_model=Carrier)
def get_carrier(carrier_id: int):
    carrier = next((c for c in carriers if c.id == carrier_id), None)
    if not carrier:
        raise HTTPException(status_code=404, detail="Carrier not found")
    return carrier

@app.put("/carriers/{carrier_id}", response_model=Carrier)
def update_carrier(carrier_id: int, carrier_update: CarrierCreate):
    carrier = next((c for c in carriers if c.id == carrier_id), None)
    if not carrier:
        raise HTTPException(status_code=404, detail="Carrier not found")
    if carrier_update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")

    carrier.code = carrier_update.code
    carrier.name = carrier_update.name
    carrier.max_weight_capacity = carrier_update.max_weight_capacity
    carrier.status = carrier_update.status
    return carrier

@app.delete("/carriers/{carrier_id}")
def delete_carrier(carrier_id: int):
    global carriers
    carrier = next((c for c in carriers if c.id == carrier_id), None)
    if not carrier:
        raise HTTPException(status_code=404, detail="Carrier not found")
    carriers = [c for c in carriers if c.id != carrier_id]
    return {"message": "Carrier deleted"}

@app.post("/shipments", response_model=Shipment)
def create_shipment(shipment: ShipmentCreate):
    carrier = next((c for c in carriers if c.id == shipment.carrier_id), None)
    if not carrier:
        raise HTTPException(status_code=400, detail="Carrier not found")
    if carrier.status != "ACTIVE":
        raise HTTPException(status_code=400, detail="Carrier is not active")
    if shipment.total_weight > carrier.max_weight_capacity:
        raise HTTPException(status_code=400, detail="Exceeds carrier capacity")
    if shipment.shift not in valid_shifts:
        raise HTTPException(status_code=400, detail="Invalid shift")

    conflict = next((s for s in shipments if s.carrier_id == shipment.carrier_id and
                     s.dispatch_date == shipment.dispatch_date and s.shift == shipment.shift), None)
    if conflict:
        raise HTTPException(status_code=400, detail="Carrier already has a shipment in this date & shift")

    new_shipment = Shipment(id=len(shipments) + 1, **shipment.dict())
    shipments.append(new_shipment)
    return new_shipment

@app.get("/shipments", response_model=List[Shipment])
def list_shipments():
    return shipments
