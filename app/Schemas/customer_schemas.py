from pydantic import BaseModel
from typing import Optional

# Base properties shared by all schemas 
class CustomerBase(BaseModel):
    customerName: str
    contactLastName: str
    contactFirstName: str
    phone: str
    addressLine1: str
    addressLine2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: str
    salesRepEmployeeNumber: Optional[int] = None
    creditLimit: Optional[float] = None

# Schema for creating a new customer (No ID needed yet) 
class CustomerCreate(CustomerBase):
    pass

# Schema for updating a customer (All fields optional) 
class CustomerUpdate(CustomerBase):
    customerName: Optional[str] = None
    contactLastName: Optional[str] = None
    contactFirstName: Optional[str] = None
    phone: Optional[str] = None
    addressLine1: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

# Schema for what the user sees (Includes the ID) 
class CustomerOut(CustomerBase):
    customerNumber: int

    class Config:
        from_attributes = True # Tells Pydantic to read SQLAlchemy models