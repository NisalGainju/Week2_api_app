import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models
from app.Schemas.payment_schemas import PaymentCreate, PaymentUpdate
from fastapi import HTTPException

async def get_payments(db: AsyncSession, skip: int = 0, limit: int = 100):
    logging.info(f"CRUD: Listing payments (skip={skip}, limit={limit})")
    result = await db.execute(select(models.Payment).offset(skip).limit(limit))
    return result.scalars().all()

async def get_payment(db: AsyncSession, customer_number: int, check_number: str):
    logging.info(f"CRUD: Fetching payment {customer_number}/{check_number}")
    result = await db.execute(
        select(models.Payment).filter(
            models.Payment.customerNumber == customer_number,
            models.Payment.checkNumber == check_number
        )
    )
    db_payment = result.scalars().first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment record not found")
    return db_payment

async def get_payments_by_customer(db: AsyncSession, customer_number: int):
    logging.info(f"CRUD: Fetching payments for customer {customer_number}")
    result = await db.execute(select(models.Payment).filter(models.Payment.customerNumber == customer_number))
    return result.scalars().all()

async def create_payment(db: AsyncSession, data: PaymentCreate):
    logging.info(f"CRUD: Recording payment for customer {data.customerNumber}")
    db_payment = models.Payment(**data.model_dump())
    db.add(db_payment)
    try:
        await db.commit()
        await db.refresh(db_payment)
        return db_payment
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=422, detail="Invalid customerNumber FK")

async def update_payment(db: AsyncSession, customer_number: int, check_number: str, data: PaymentUpdate):
    db_payment = await get_payment(db, customer_number, check_number)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(db_payment, key, value)
    await db.commit()
    await db.refresh(db_payment)
    return db_payment

async def delete_payment(db: AsyncSession, customer_number: int, check_number: str):
    db_payment = await get_payment(db, customer_number, check_number)
    await db.delete(db_payment)
    await db.commit()
    return {"message": "Payment record deleted successfully"}