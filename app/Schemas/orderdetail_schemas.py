from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class OrderDetailBase(BaseModel):
    # quantityOrdered must be > 0
    quantityOrdered: int = Field(..., gt=0)
    priceEach: Decimal
    # orderLineNumber must be between 1 and 32767 (smallint)
    orderLineNumber: int = Field(..., ge=1, le=32767)

class OrderDetailCreate(OrderDetailBase):
    orderNumber: int
    productCode: str

class OrderDetailOut(OrderDetailBase):
    orderNumber: int
    productCode: str
    class Config:
        from_attributes = True

class OrderDetailUpdate(BaseModel):
    quantityOrdered: Optional[int] = Field(None, gt=0)
    priceEach: Optional[Decimal] = None
    orderLineNumber: Optional[int] = Field(None, ge=1, le=32767)