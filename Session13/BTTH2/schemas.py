from pydantic import BaseModel, Field, validator
from typing import Optional

class BoardingSlotCreate(BaseModel):
    slot_number: str = Field(..., max_length=50)
    room_size: str = Field(..., min_length=1)
    price_per_day: float = Field(..., gt=0)
    status: Optional[str] = Field(default="VACANT")

    @validator("room_size")
    def validate_room_size(cls, v):
        if v not in ["SMALL", "MEDIUM", "LARGE"]:
            raise ValueError("Room size must be SMALL, MEDIUM, or LARGE")
        return v

    @validator("status")
    def validate_status(cls, v):
        if v not in ["VACANT", "OCCUPIED"]:
            raise ValueError("Status must be VACANT or OCCUPIED")
        return v

class BoardingSlotUpdate(BaseModel):
    slot_number: Optional[str]
    room_size: Optional[str]
    price_per_day: Optional[float]
    status: Optional[str]

    @validator("room_size")
    def validate_room_size(cls, v):
        if v and v not in ["SMALL", "MEDIUM", "LARGE"]:
            raise ValueError("Room size must be SMALL, MEDIUM, or LARGE")
        return v

    @validator("status")
    def validate_status(cls, v):
        if v and v not in ["VACANT", "OCCUPIED"]:
            raise ValueError("Status must be VACANT or OCCUPIED")
        return v

class BoardingSlotResponse(BaseModel):
    id: int
    slot_number: str
    room_size: str
    price_per_day: float
    status: str

    class Config:
        from_attributes = True
