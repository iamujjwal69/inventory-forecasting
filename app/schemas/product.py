from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    category: Optional[str] = None
    price: float
    current_stock: Optional[int] = 0
    reorder_level: Optional[int] = 10
    supplier_id: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    current_stock: Optional[int] = None
    reorder_level: Optional[int] = None
    supplier_id: Optional[int] = None

class ProductResponse(ProductBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
