from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import database
from app.Crud import orderdetail_crud as crud
from app.Schemas import orderdetail_schemas as schemas


router = APIRouter()

@router.get("/", response_model=list[schemas.OrderDetailOut])
async def read_order_details(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)):
    return await crud.get_order_details(db, skip, limit)

@router.get("/{orderNumber}/{productCode}", response_model=schemas.OrderDetailOut)
async def read_specific_detail(orderNumber: int, productCode: str, db: AsyncSession = Depends(database.get_db)):
    return await crud.get_order_detail(db, orderNumber, productCode)

@router.get("/order/{orderNumber}", response_model=list[schemas.OrderDetailOut])
async def read_by_order(orderNumber: int, db: AsyncSession = Depends(database.get_db)):
    return await crud.get_details_by_order(db, order_number=orderNumber)

@router.get("/product/{productCode}", response_model=list[schemas.OrderDetailOut])
async def read_by_product(productCode: str, db: AsyncSession = Depends(database.get_db)):
    return await crud.get_details_by_product(db, product_code=productCode)

@router.post("/", response_model=schemas.OrderDetailOut)
async def create_detail(data: schemas.OrderDetailCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.create_order_detail(db, data=data)

@router.put("/{orderNumber}/{productCode}", response_model=schemas.OrderDetailOut)
async def update_detail(orderNumber: int, productCode: str, data: schemas.OrderDetailUpdate, db: AsyncSession = Depends(database.get_db)):
    return await crud.update_order_detail(db, orderNumber, productCode, data)

@router.delete("/{orderNumber}/{productCode}")
async def delete_detail(orderNumber: int, productCode: str, db: AsyncSession = Depends(database.get_db)):
    return await crud.delete_order_detail(db, orderNumber, productCode)