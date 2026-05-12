from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import database
from app.Crud import product_crud as crud
from app.Schemas import product_schemas as schemas
import logging

router = APIRouter()

@router.get("/", response_model=list[schemas.ProductOut])
async def read_products(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)):
    logging.info("API: GET /products accessed") 
    return await crud.get_products(db, skip=skip, limit=limit)

@router.get("/{productCode}", response_model=schemas.ProductOut)
async def read_product(productCode: str, db: AsyncSession = Depends(database.get_db)):
    logging.info(f"API: GET /products/{productCode} accessed") 
    return await crud.get_product(db, product_code=productCode)

@router.post("/", response_model=schemas.ProductOut)
async def create_new_product(product: schemas.ProductCreate, db: AsyncSession = Depends(database.get_db)):
    logging.info(f"API: POST /products for {product.productCode}") 
    return await crud.create_product(db, product_data=product)



@router.put("/{productCode}", response_model=schemas.ProductOut)
async def update_existing_product(
    productCode: str, 
    product: schemas.ProductUpdate, 
    db: AsyncSession = Depends(database.get_db)
):
    logging.info(f"API: PUT /products/{productCode} accessed")
    return await crud.update_product(db, product_code=productCode, product_data=product)

@router.delete("/{productCode}")
async def delete_existing_product(productCode: str, db: AsyncSession = Depends(database.get_db)):
    logging.info(f"API: DELETE /products/{productCode} accessed")
    return await crud.delete_product(db, product_code=productCode)