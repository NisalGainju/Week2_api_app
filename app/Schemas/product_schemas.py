from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class ProductBase(BaseModel):
    productName: str
    productLine: str
    productScale: str
    productVendor: str
    productDescription: str
    quantityInStock: int = Field(..., ge=0)  # ge=0 ensures stock isn't negative
    buyPrice: Decimal
    MSRP: Decimal

class ProductCreate(ProductBase):
    productCode: str  # String PK, up to 15 chars

class ProductOut(ProductBase):
    productCode: str
    
    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    productName: Optional[str] = None
    productLine: Optional[str] = None
    quantityInStock: Optional[int] = None
    buyPrice: Optional[Decimal] = None
    MSRP: Optional[Decimal] = None