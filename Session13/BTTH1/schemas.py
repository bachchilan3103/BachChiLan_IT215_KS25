from pydantic import BaseModel, Field, validator
from typing import Optional

class MenuItemCreate(BaseModel):
    dish_code: str = Field(..., max_length=50)
    dish_name: str = Field(..., min_length=1)
    calorie_count: int = Field(..., gt=0)
    price: float = Field(..., gt=0)
    status: Optional[str] = Field(default="AVAILABLE")

    @validator("status")
    def validate_status(cls, v):
        if v not in ["AVAILABLE", "OUT_OF_STOCK"]:
            raise ValueError("Status must be AVAILABLE or OUT_OF_STOCK")
        return v


class MenuItemUpdate(BaseModel):
    dish_code: Optional[str]
    dish_name: Optional[str]
    calorie_count: Optional[int]
    price: Optional[float]
    status: Optional[str]

    @validator("status")
    def validate_status(cls, v):
        if v and v not in ["AVAILABLE", "OUT_OF_STOCK"]:
            raise ValueError("Status must be AVAILABLE or OUT_OF_STOCK")
        return v


class MenuItemResponse(BaseModel):
    id: int
    dish_code: str
    dish_name: str
    calorie_count: int
    price: float
    status: str

    class Config:
        from_attributes = True
