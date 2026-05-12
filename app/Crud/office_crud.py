import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models 
from app.Schemas.office_schemas import OfficeCreate, OfficeUpdate 
from fastapi import HTTPException 

async def get_offices(db: AsyncSession, skip: int = 0, limit: int = 100):
    logging.info(f"CRUD: Fetching offices (skip={skip}, limit={limit})") 
    result = await db.execute(select(models.Office).offset(skip).limit(limit)) 
    return result.scalars().all() 

async def get_office(db: AsyncSession, id: str):
    logging.info(f"CRUD: Fetching office by ID: {id}") 
    result = await db.execute(select(models.Office).filter(models.Office.officeCode == id)) 
    db_office = result.scalars().first() 
    if not db_office:
        raise HTTPException(status_code=404, detail="Office not found") 
    return db_office



# READ: Get office with related employees 
async def get_offices_with_employees(db: AsyncSession, id: str):
    logging.info(f"CRUD: Fetching office {id} with employee list ")
    # Use selectinload or joinedload depending on your model relationships
    result = await db.execute(
        select(models.Office).filter(models.Office.officeCode == id)
    )
    db_office = result.scalars().first()
    if not db_office:
        raise HTTPException(status_code=404, detail="Office not found [cite: 194]")
    
    # In a real scenario, ensure your SQLAlchemy model has the relationship 'employees'
    return db_office


async def create_office(db: AsyncSession, data: OfficeCreate):
    logging.info(f"CRUD: Creating new office {data.officeCode}") 
    db_office = models.Office(**data.model_dump()) 
    db.add(db_office)
    await db.commit()
    await db.refresh(db_office)
    return db_office

async def update_office(db: AsyncSession, id: str, data: OfficeUpdate):
    logging.info(f"CRUD: Updating office {id}") 
    db_office = await get_office(db, id)
    update_data = data.model_dump(exclude_unset=True) 
    for key, value in update_data.items():
        setattr(db_office, key, value)
    await db.commit()
    await db.refresh(db_office)
    return db_office

async def delete_office(db: AsyncSession, id: str):
    logging.info(f"CRUD: Deleting office {id}") 
    db_office = await get_office(db, id)
    try:
        await db.delete(db_office)
        await db.commit()
        return {"message": "Office deleted successfully"} 
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Fails if employees still reference it") 