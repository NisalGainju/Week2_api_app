from pydantic import BaseModel, EmailStr
from typing import Optional

class EmployeeBase(BaseModel):
    lastName: str
    firstName: str
    extension: str
    email: EmailStr
    officeCode: str
    reportsTo: Optional[int] = None
    jobTitle: str

class EmployeeCreate(EmployeeBase):
    employeeNumber: int

class EmployeeOut(EmployeeBase):
    employeeNumber: int
    class Config:
        from_attributes = True

class EmployeeUpdate(BaseModel):
    lastName: Optional[str] = None
    firstName: Optional[str] = None
    extension: Optional[str] = None
    email: Optional[EmailStr] = None
    officeCode: Optional[str] = None
    reportsTo: Optional[int] = None
    jobTitle: Optional[str] = None