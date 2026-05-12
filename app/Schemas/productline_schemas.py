from pydantic import BaseModel
from typing import Optional

class ProductLineBase(BaseModel):
    textDescription: Optional[str] = None
    htmlDescription: Optional[str] = None
    # We leave 'image' out of the basic Create/Out for simplicity 

class ProductLineCreate(ProductLineBase):
    productLine: str # Primary Key provided by the user 

class ProductLineOut(ProductLineBase):
    productLine: str
    class Config:
        from_attributes = True

class ProductLineUpdate(ProductLineBase):
    pass # All fields in Base are already Optional