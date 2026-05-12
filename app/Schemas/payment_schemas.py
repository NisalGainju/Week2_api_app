from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date
from decimal import Decimal

class PaymentBase(BaseModel):
    paymentDate: date
    amount: Decimal = Field(..., gt=0) # Must be strictly positive

    @field_validator('paymentDate')
    @classmethod
    def validate_payment_date(cls, v: date):
        if v > date.today():
            raise ValueError('paymentDate cannot be in the future')
        return v

class PaymentCreate(PaymentBase):
    customerNumber: int
    checkNumber: str # Note: This is a string, not an integer

class PaymentOut(PaymentBase):
    customerNumber: int
    checkNumber: str
    class Config:
        from_attributes = True

class PaymentUpdate(BaseModel):
    paymentDate: Optional[date] = None
    amount: Optional[Decimal] = Field(None, gt=0)