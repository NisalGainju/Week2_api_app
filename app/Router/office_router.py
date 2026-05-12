from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import database 
from app.Crud import office_crud as crud 
from app.Schemas import office_schemas as schemas 
import logging

router = APIRouter()

# Endpoint 1: List all offices 
@router.get("/", response_model=list[schemas.OfficeOut])
async def read_offices(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)):
    return await crud.get_offices(db, skip=skip, limit=limit)

# Endpoint 2: Get single office 
@router.get("/{officeCode}", response_model=schemas.OfficeOut)
async def read_office(officeCode: str, db: AsyncSession = Depends(database.get_db)):
    return await crud.get_office(db, id=officeCode)

# Endpoint 3: Get office with employees 
@router.get("/{officeCode}/employees")
async def read_office_employees(officeCode: str, db: AsyncSession = Depends(database.get_db)):
    logging.info(f"API: GET /offices/{officeCode}/employees accessed ")
    return await crud.get_offices_with_employees(db, id=officeCode) 

@router.post("/", response_model=schemas.OfficeOut)
async def create_new_office(office: schemas.OfficeCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.create_office(db, data=office) 

@router.put("/{officeCode}", response_model=schemas.OfficeOut)
async def update_office_data(officeCode: str, office: schemas.OfficeUpdate, db: AsyncSession = Depends(database.get_db)):
    return await crud.update_office(db, id=officeCode, data=office) 

@router.delete("/{officeCode}")
async def delete_existing_office(officeCode: str, db: AsyncSession = Depends(database.get_db)):
    return await crud.delete_office(db, id=officeCode) 