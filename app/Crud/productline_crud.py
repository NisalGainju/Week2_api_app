import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models
from app.Schemas.productline_schemas import ProductLineCreate, ProductLineUpdate
from fastapi import HTTPException

async def get_productlines(db: AsyncSession, skip: int = 0, limit: int = 100):
    logging.info(f"CRUD: Listing product lines [cite: 144]")
    result = await db.execute(select(models.ProductLine).offset(skip).limit(limit))
    return result.scalars().all()

async def get_productline(db: AsyncSession, product_line: str):
    result = await db.execute(select(models.ProductLine).filter(models.ProductLine.productLine == product_line))
    db_pl = result.scalars().first()
    if not db_pl:
        raise HTTPException(status_code=404, detail="ProductLine not found [cite: 150]")
    return db_pl

async def create_productline(db: AsyncSession, pl_data: ProductLineCreate):
    db_pl = models.ProductLine(**pl_data.model_dump())
    db.add(db_pl)
    await db.commit()
    await db.refresh(db_pl)
    return db_pl


async def update_productline(db: AsyncSession, product_line: str, pl_data: ProductLineUpdate):
    logging.info(f"CRUD: Updating product line: {product_line} ")
    
    # Reuse the read-by-PK logic to ensure the record exists [cite: 144]
    db_pl = await get_productline(db, product_line)
    
    # Convert Pydantic model to dict, excluding fields the user didn't send 
    update_data = pl_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_pl, key, value)
    
    await db.commit()
    await db.refresh(db_pl)
    return db_pl


async def delete_productline(db: AsyncSession, product_line: str):
    db_pl = await get_productline(db, product_line)
    try:
        await db.delete(db_pl)
        await db.commit()
    except Exception:
        await db.rollback()
        # Custom rule: fail if products still reference it [cite: 159, 164]
        raise HTTPException(status_code=409, detail="Cannot delete: Products reference this line [cite: 165]")
    return {"message": "Deleted successfully"}