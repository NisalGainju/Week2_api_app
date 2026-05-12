from pydantic import BaseModel, field_validator
from typing import Optional, Literal
from datetime import date

class OrderBase(BaseModel):
    orderDate: date
    requiredDate: date
    shippedDate: Optional[date] = None
    # Validating 6 specific status values
    status: Literal['Shipped', 'Resolved', 'Cancelled', 'On Hold', 'Disputed', 'In Process']
    comments: Optional[str] = None
    customerNumber: int

    @field_validator('requiredDate')
    @classmethod
    def validate_dates(cls, v: date, info):
        if 'orderDate' in info.data and v < info.data['orderDate']:
            raise ValueError('requiredDate must be after orderDate')
        return v

class OrderCreate(OrderBase):
    orderNumber: int

class OrderOut(OrderBase):
    orderNumber: int
    class Config:
        from_attributes = True

class OrderUpdate(BaseModel):
    orderDate: Optional[date] = None
    requiredDate: Optional[date] = None
    shippedDate: Optional[date] = None
    status: Optional[Literal['Shipped', 'Resolved', 'Cancelled', 'On Hold', 'Disputed', 'In Process']] = None
    comments: Optional[str] = None
    customerNumber: Optional[int] = None