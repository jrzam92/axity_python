from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class OrderBase(BaseModel):
    customer_name: str = Field(..., min_length=3, max_length=100)
    product: str = Field(..., min_length=3, max_length=200)
    quantity: int = Field(..., gt=0, description="Debe ser mayor a 0")
    price: float = Field(..., gt=0)
    status: str = Field(default="pending", pattern="^(pending|completed|cancelled)$")
    
    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('El precio debe ser positivo')
        return round(v, 2)

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    customer_name: Optional[str] = Field(None, min_length=3, max_length=100)
    product: Optional[str] = None
    quantity: Optional[int] = Field(None, gt=0)
    price: Optional[float] = Field(None, gt=0)
    status: Optional[str] = Field(None, pattern="^(pending|completed|cancelled)$")

class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True  # Para compatibilidad con SQLAlchemy

class OrderListResponse(BaseModel):
    total: int
    orders: list[OrderResponse]