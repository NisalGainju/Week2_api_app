import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models
from app.Schemas.employee_schemas import EmployeeCreate, EmployeeUpdate
from fastapi import HTTPException

async def get_employees(db: AsyncSession, skip: int = 0, limit: int = 100):
    logging.info(f"CRUD: Listing employees (skip={skip}, limit={limit})")
    result = await db.execute(select(models.Employee).offset(skip).limit(limit))
    return result.scalars().all()

async def get_employee(db: AsyncSession, id: int):
    logging.info(f"CRUD: Fetching employee {id}")
    result = await db.execute(select(models.Employee).filter(models.Employee.employeeNumber == id))
    db_emp = result.scalars().first()
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_emp

async def get_employee_with_customers(db: AsyncSession, id: int):
    logging.info(f"CRUD: Fetching employee {id} with managed customers")
    # Verify employee exists first
    return await get_employee(db, id)

async def create_employee(db: AsyncSession, data: EmployeeCreate):
    logging.info(f"CRUD: Creating employee {data.employeeNumber}")
    db_emp = models.Employee(**data.model_dump())
    db.add(db_emp)
    try:
        await db.commit()
        await db.refresh(db_emp)
        return db_emp
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=422, detail="Invalid officeCode or reportsTo FKs")

async def update_employee(db: AsyncSession, id: int, data: EmployeeUpdate):
    logging.info(f"CRUD: Updating employee {id}")
    db_emp = await get_employee(db, id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(db_emp, key, value)
    await db.commit()
    await db.refresh(db_emp)
    return db_emp

async def delete_employee(db: AsyncSession, id: int):
    logging.info(f"CRUD: Deleting employee {id}")
    db_emp = await get_employee(db, id)
    try:
        await db.delete(db_emp)
        await db.commit()
        return {"message": "Employee deleted successfully"}
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Fails if they have direct reports or customers")