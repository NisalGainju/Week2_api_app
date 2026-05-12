from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import database
from app.Crud import productline_crud as crud
from app.Schemas import productline_schemas as schemas

router = APIRouter()

@router.get("/", response_model=list[schemas.ProductLineOut])
async def read_productlines(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)):
    return await crud.get_productlines(db, skip=skip, limit=limit)

@router.get("/{productLine}", response_model=schemas.ProductLineOut)
async def read_productline(productLine: str, db: AsyncSession = Depends(database.get_db)):
    """Get a single product line by name. 404 if not found."""
    return await crud.get_productline(db, product_line=productLine)

@router.post("/", response_model=schemas.ProductLineOut)
async def create_new_productline(pl: schemas.ProductLineCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.create_productline(db, pl_data=pl)

@router.delete("/{productLine}")
async def delete_line(productLine: str, db: AsyncSession = Depends(database.get_db)):
    return await crud.delete_productline(db, product_line=productLine)

@router.put("/{productLine}", response_model=schemas.ProductLineOut)
async def update_existing_productline(
    productLine: str, 
    pl: schemas.ProductLineUpdate, 
    db: AsyncSession = Depends(database.get_db)
):
    return await crud.update_productline(db, product_line=productLine, pl_data=pl)