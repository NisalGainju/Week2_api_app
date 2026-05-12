from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import database
from app.Crud import payment_crud as crud
from app.Schemas import payment_schemas as schemas


import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=list[schemas.PaymentOut])
async def read_payments(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)):
    logging.info("API: GET /payments accessed")
    return await crud.get_payments(db, skip, limit)

@router.get("/{customerNumber}/{checkNumber}", response_model=schemas.PaymentOut)
async def read_specific_payment(customerNumber: int, checkNumber: str, db: AsyncSession = Depends(database.get_db)):
    logging.info(f"API: GET /payments/{customerNumber}/{checkNumber} accessed")
    return await crud.get_payment(db, customerNumber, checkNumber)

@router.get("/customer/{customerNumber}", response_model=list[schemas.PaymentOut])
async def read_customer_payments(customerNumber: int, db: AsyncSession = Depends(database.get_db)):
    logging.info(f"API: GET /payments/customer/{customerNumber} accessed")
    return await crud.get_payments_by_customer(db, customer_number=customerNumber)

@router.post("/", response_model=schemas.PaymentOut)
async def record_payment(data: schemas.PaymentCreate, db: AsyncSession = Depends(database.get_db)):
    logging.info(f"API: POST /payments for customer {data.customerNumber}")
    return await crud.create_payment(db, data=data)

@router.put("/{customerNumber}/{checkNumber}", response_model=schemas.PaymentOut)
async def update_payment_record(customerNumber: int, checkNumber: str, data: schemas.PaymentUpdate, db: AsyncSession = Depends(database.get_db)):
    logging.info(f"API: PUT /payments/{customerNumber}/{checkNumber} accessed")
    return await crud.update_payment(db, customer_number=customerNumber, check_number=checkNumber, data=data)

@router.delete("/{customerNumber}/{checkNumber}")
async def delete_payment_record(customerNumber: int, checkNumber: str, db: AsyncSession = Depends(database.get_db)):
    logging.info(f"API: DELETE /payments/{customerNumber}/{checkNumber} accessed")
    return await crud.delete_payment(db, customer_number=customerNumber, check_number=checkNumber)