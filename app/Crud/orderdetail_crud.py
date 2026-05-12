import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models
from app.Schemas.orderdetail_schemas import OrderDetailCreate, OrderDetailUpdate
from fastapi import HTTPException

async def get_order_details(db: AsyncSession, skip: int = 0, limit: int = 100):
    logging.info(f"CRUD: Listing all order details")
    result = await db.execute(select(models.OrderDetail).offset(skip).limit(limit))
    return result.scalars().all()

async def get_order_detail(db: AsyncSession, order_number: int, product_code: str):
    logging.info(f"CRUD: Fetching line item {order_number}/{product_code}")
    result = await db.execute(
        select(models.OrderDetail).filter(
            models.OrderDetail.orderNumber == order_number,
            models.OrderDetail.productCode == product_code
        )
    )
    db_item = result.scalars().first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Order detail not found")
    return db_item

async def get_details_by_order(db: AsyncSession, order_number: int):
    result = await db.execute(select(models.OrderDetail).filter(models.OrderDetail.orderNumber == order_number))
    return result.scalars().all()

async def get_details_by_product(db: AsyncSession, product_code: str):
    result = await db.execute(select(models.OrderDetail).filter(models.OrderDetail.productCode == product_code))
    return result.scalars().all()

async def create_order_detail(db: AsyncSession, data: OrderDetailCreate):
    logging.info(f"CRUD: Adding item {data.productCode} to order {data.orderNumber}")
    db_item = models.OrderDetail(**data.model_dump())
    db.add(db_item)
    try:
        await db.commit()
        await db.refresh(db_item)
        return db_item
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=422, detail="Invalid orderNumber or productCode")

async def update_order_detail(db: AsyncSession, order_number: int, product_code: str, data: OrderDetailUpdate):
    db_item = await get_order_detail(db, order_number, product_code)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(db_item, key, value)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def delete_order_detail(db: AsyncSession, order_number: int, product_code: str):
    db_item = await get_order_detail(db, order_number, product_code)
    await db.delete(db_item)
    await db.commit()
    return {"message": "Line item removed"}