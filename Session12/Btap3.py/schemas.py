from pydantic import BaseModel

class ShipmentUpdate(BaseModel):
    receiver_name: str
    delivery_address: str

class ShipmentResponse(BaseModel):
    id: int
    tracking_code: str
    receiver_name: str
    delivery_address: str

    class Config:
        orm_mode = True
