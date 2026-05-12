import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Product  # Ensure Product is defined in models.py
from app.Schemas.product_schemas import ProductCreate, ProductUpdate

async def get_products(db: AsyncSession, skip: int = 0, limit: int = 100):
    logging.info(f"CRUD: Fetching products (skip={skip}, limit={limit})")
    result = await db.execute(select(Product).offset(skip).limit(limit))
    return result.scalars().all()

async def get_product(db: AsyncSession, product_code: str):
    logging.info(f"CRUD: Searching for product {product_code}")
    result = await db.execute(select(Product).filter(Product.productCode == product_code))
    return result.scalars().first()

async def create_product(db: AsyncSession, product_data: ProductCreate):
    logging.info(f"CRUD: Creating product {product_data.productCode}")
    db_product = Product(**product_data.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def update_product(db: AsyncSession, product_code: str, product_data: ProductUpdate):
    logging.info(f"CRUD: Updating product {product_code}")
    db_product = await get_product(db, product_code) # Reuses our search logic
    
    # Convert Pydantic model to dict, excluding unset fields
    update_data = product_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def delete_product(db: AsyncSession, product_code: str):
    logging.info(f"CRUD: Deleting product {product_code}")
    db_product = await get_product(db, product_code)
    await db.delete(db_product)
    await db.commit()
    return {"message": f"Product {product_code} deleted successfully"}