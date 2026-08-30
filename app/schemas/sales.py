from pydantic import BaseModel
from datetime import date
from typing import Optional

class SaleBase(BaseModel):
    product_id: int
    sale_date: date
    quantity: int
    unit_price: float

class SaleCreate(SaleBase):
    pass

class SaleResponse(SaleBase):
    id: int

    class Config:
        orm_mode = True
