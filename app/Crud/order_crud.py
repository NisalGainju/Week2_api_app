import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models
from fastapi import HTTPException

async def get_orders(db: AsyncSession, skip: int = 0, limit: int = 100):
    logging.info(f"CRUD: Listing orders (skip={skip}, limit={limit})")
    result = await db.execute(select(models.Order).offset(skip).limit(limit))
    return result.scalars().all()

async def get_order(db: AsyncSession, id: int):
    logging.info(f"CRUD: Fetching order {id}")
    result = await db.execute(select(models.Order).filter(models.Order.orderNumber == id))
    db_order = result.scalars().first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

async def get_orders_by_customer(db: AsyncSession, customer_number: int):
    logging.info(f"CRUD: Fetching orders for customer {customer_number}")
    result = await db.execute(select(models.Order).filter(models.Order.customerNumber == customer_number))
    return result.scalars().all()

async def create_order(db: AsyncSession, data):
    logging.info(f"CRUD: Creating order {data.orderNumber}")
    db_order = models.Order(**data.model_dump())
    db.add(db_order)
    try:
        await db.commit()
        await db.refresh(db_order)
        return db_order
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=422, detail="Invalid customerNumber FK")

async def delete_order(db: AsyncSession, id: int):
    logging.info(f"CRUD: Deleting order {id}")
    db_order = await get_order(db, id)
    try:
        await db.delete(db_order)
        await db.commit()
        return {"message": "Deleted successfully"}
    except Exception:
        await db.rollback()
        # Return 409 Conflict as required by the image notes
        raise HTTPException(status_code=409, detail="Order has orderdetails rows")