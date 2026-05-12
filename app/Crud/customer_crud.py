import logging
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.Schemas import customer_schemas as schemas
from app import models
from sqlalchemy import func

# 1. Read many customers with Pagination (Skip/Limit)
async def get_customers(db: Session, skip: int = 0, limit: int = 100):
    """
    Fetches a list of customers with pagination.
    """
    logging.info(f"CRUD: Fetching customers with skip={skip}, limit={limit}") 
    result = await db.execute(select(models.Customer).offset(skip).limit(limit))
    return result.scalars().all()

# 2. Read a single customer by ID
async def get_customer(db: Session, customer_number: int):
    """
    Searches the database for a specific customer ID. 
    """
    logging.info(f"CRUD: Searching for customerNumber {customer_number}") 
    result = await db.execute(
        select(models.Customer).filter(models.Customer.customerNumber == customer_number)
    )
    customer = result.scalars().first()
    
    if not customer:
        logging.warning(f"CRUD: Customer {customer_number} not found") 
    
    return customer




# 3. Create a new customer
async def create_customer(db: Session, customer: schemas.CustomerCreate):
    logging.info(f"CRUD: Creating new customer {customer.customerName}") 
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    await db.commit()
    await db.refresh(db_customer)
    return db_customer

# 4. Update an existing customer
async def update_customer(db: Session, customer_number: int, customer_data: schemas.CustomerUpdate):
    logging.info(f"CRUD: Updating customer {customer_number}") 
    result = await db.execute(select(models.Customer).filter(models.Customer.customerNumber == customer_number))
    db_customer = result.scalars().first()
    
    if db_customer:
        # Only update fields that were actually sent 
        update_data = customer_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_customer, key, value)
        await db.commit()
        await db.refresh(db_customer)
    return db_customer

# 5. Delete a customer
async def delete_customer(db: Session, customer_number: int):
    logging.info(f"CRUD: Deleting customer {customer_number}") 
    result = await db.execute(select(models.Customer).filter(models.Customer.customerNumber == customer_number))
    db_customer = result.scalars().first()
    
    if db_customer:
        await db.delete(db_customer)
        await db.commit()
        return True
    return False






# Example for Customers - Repeat this logic for all 8 tables
async def get_customers_count(db:Session):
    logging.info("CRUD: Starting count query for Customers") 
    result = await db.execute(select(func.count()).select_from(models.Customer))
    count = result.scalar()
    logging.info(f"CRUD: Completed count for Customers: {count}") 
    return count

async def get_orders_count(db: Session):
    result = await db.execute(select(func.count()).select_from(models.Order))
    return result.scalar()

async def get_products_count(db: Session):
    result = await db.execute(select(func.count()).select_from(models.Product))
    return result.scalar()

async def get_employees_count(db: Session):
    result = await db.execute(select(func.count()).select_from(models.Employee))
    return result.scalar()

async def get_offices_count(db:Session):
    result = await db.execute(select(func.count()).select_from(models.Office))
    return result.scalar()

async def get_payments_count(db: Session):
    result = await db.execute(select(func.count()).select_from(models.Payment))
    return result.scalar()

async def get_orderdetails_count(db: Session):
    result = await db.execute(select(func.count()).select_from(models.OrderDetail))
    return result.scalar()

async def get_productlines_count(db: Session):
    result = await db.execute(select(func.count()).select_from(models.ProductLine))
    return result.scalar()