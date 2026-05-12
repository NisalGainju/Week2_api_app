from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import database
from app.Crud import order_crud as crud
from app.Schemas import order_schemas as schemas

router = APIRouter()

@router.get("/", response_model=list[schemas.OrderOut])
async def read_orders(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)):
    return await crud.get_orders(db, skip, limit)

@router.get("/{orderNumber}", response_model=schemas.OrderOut)
async def read_order(orderNumber: int, db: AsyncSession = Depends(database.get_db)):
    return await crud.get_order(db, id=orderNumber)

@router.get("/{orderNumber}/orderdetails")
async def read_order_details(orderNumber: int, db: AsyncSession = Depends(database.get_db)):
    # This fetches the order object; the relationship handles the details
    return await crud.get_order(db, id=orderNumber)

@router.get("/customer/{customerNumber}", response_model=list[schemas.OrderOut])
async def read_customer_orders(customerNumber: int, db: AsyncSession = Depends(database.get_db)):
    # Per notes: returns [] if no orders, never 404
    return await crud.get_orders_by_customer(db, customer_number=customerNumber)

@router.post("/", response_model=schemas.OrderOut)
async def create_order(order: schemas.OrderCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.create_order(db, data=order)

@router.put("/{orderNumber}", response_model=schemas.OrderOut)
async def update_order(orderNumber: int, order: schemas.OrderUpdate, db: AsyncSession = Depends(database.get_db)):
    # Logic similar to previous PUT implementations
    return await crud.update_order(db, id=orderNumber, data=order)

@router.delete("/{orderNumber}")
async def delete_order(orderNumber: int, db: AsyncSession = Depends(database.get_db)):
    return await crud.delete_order(db, id=orderNumber)