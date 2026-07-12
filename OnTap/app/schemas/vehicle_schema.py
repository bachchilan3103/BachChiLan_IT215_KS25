from pydantic import BaseModel, Field, field_validator

class VehicleBase(BaseModel):
    brand: str = Field(..., min_length=2, max_length=50)
    model: str
    daily_rate: float = Field(..., gt=0)
    production_year: int = Field(..., ge=2010, le=2026)
    status: str = Field(default="available")

    @field_validator("status")
    def validate_status(cls, v):
        allowed = ["available", "rented", "maintenance"]
        if v not in allowed:
            raise ValueError(f"Status must be one of {allowed}")
        return v

class VehicleCreate(VehicleBase):
    id: str

class VehicleUpdate(VehicleBase):
    pass
