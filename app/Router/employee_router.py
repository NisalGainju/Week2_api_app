from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import database, models
from app.Crud import employee_crud as crud
from app.Schemas import employee_schemas as schemas

router = APIRouter()

@router.get("/", response_model=list[schemas.EmployeeOut])
async def read_employees(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)):
    return await crud.get_employees(db, skip, limit)

@router.get("/{employeeNumber}", response_model=schemas.EmployeeOut)
async def read_employee(employeeNumber: int, db: AsyncSession = Depends(database.get_db)):
    return await crud.get_employee(db, id=employeeNumber)

# GET: Employee with the list of customers they manage.
@router.get("/{employeeNumber}/customers")
async def read_employee_customers(employeeNumber: int, db: AsyncSession = Depends(database.get_db)):
    return await crud.get_employee_with_customers(db, id=employeeNumber)

# GET: All employees who report to this employee.
@router.get("/{employeeNumber}/reports", response_model=list[schemas.EmployeeOut])
async def read_employee_reports(employeeNumber: int, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(
        select(models.Employee).filter(models.Employee.reportsTo == employeeNumber)
    )
    return result.scalars().all()

# POST: Create a new employee. Validate officeCode and reportsTo FKs.
@router.post("/", response_model=schemas.EmployeeOut)
async def create_new_employee(employee: schemas.EmployeeCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.create_employee(db, data=employee)

# PUT: Update an employee. All fields optional.
@router.put("/{employeeNumber}", response_model=schemas.EmployeeOut)
async def update_employee_data(employeeNumber: int, employee: schemas.EmployeeUpdate, db: AsyncSession = Depends(database.get_db)):
    return await crud.update_employee(db, id=employeeNumber, data=employee)

# DELETE: Delete an employee. Fails if they have direct reports or customers.
@router.delete("/{employeeNumber}")
async def delete_existing_employee(employeeNumber: int, db: AsyncSession = Depends(database.get_db)):
    return await crud.delete_employee(db, id=employeeNumber)