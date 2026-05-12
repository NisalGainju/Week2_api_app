from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging
from app.Crud import customer_crud as crud
from app.Schemas import customer_schemas as schemas
from app import database

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/", response_model=List[schemas.CustomerOut])
async def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """
    Endpoint to list all customers with pagination limits. 
    """
    logging.info("API: GET request for all customers") 
    customers = await crud.get_customers(db, skip=skip, limit=limit)
    return customers


import asyncio
import time

# Add this to app/router.py
@router.get("/overall_counts", tags=["Dashboard"])
async def read_overall_counts():
    logging.info("API: Starting concurrent aggregation with independent sessions")
    start_time = time.time()

    # We define a helper function to manage its own session lifecycle
    async def get_count_with_session(crud_func):
        # Create a brand new session from your session factory
        async with database.AsyncSessionLocal() as session:
            return await crud_func(session)

    # Wrap each CRUD call in our session helper
    tasks = [
        get_count_with_session(crud.get_customers_count),
        get_count_with_session(crud.get_orders_count),
        get_count_with_session(crud.get_products_count),
        get_count_with_session(crud.get_employees_count),
        get_count_with_session(crud.get_offices_count),
        get_count_with_session(crud.get_payments_count),
        get_count_with_session(crud.get_orderdetails_count),
        get_count_with_session(crud.get_productlines_count)
    ]

    # Now they can TRULY run in parallel
    results = await asyncio.gather(*tasks)

    response_data = {
        "customers": results[0],
        "orders": results[1],
        "products": results[2],
        "employees": results[3],
        "offices": results[4],
        "payments": results[5],
        "orderdetails": results[6],
        "productlines": results[7]
    }

    process_time = time.time() - start_time
    logging.info(f"API: Concurrency successful in {process_time:.4f}s")
    return response_data


@router.get("/{customer_number}", response_model=schemas.CustomerOut)
async def read_customer(customer_number: int, db: Session = Depends(database.get_db)):
    """
    Endpoint to retrieve detailed info about a specific customer. 
    """
    logging.info(f"API: GET request for customer {customer_number}") 
    db_customer = await crud.get_customer(db, customer_number=customer_number)
    
    if db_customer is None:
        logging.error(f"API: Customer {customer_number} not found") 
        raise HTTPException(status_code=404, detail="Customer not found") 
        
    return db_customer



# Add these endpoints to your existing app/router.py

# POST: Create [cite: 149]
@router.post("/", response_model=schemas.CustomerOut, status_code=201)
async def create_new_customer(customer: schemas.CustomerCreate, db: Session = Depends(database.get_db)):
    logging.info(f"API: POST request to create customer") 
    return await crud.create_customer(db=db, customer=customer)

# PUT: Update [cite: 151]
@router.put("/{customer_number}", response_model=schemas.CustomerOut)
async def update_existing_customer(
    customer_number: int, 
    customer_data: schemas.CustomerUpdate, 
    db: Session = Depends(database.get_db)
):
    logging.info(f"API: PUT request for customer {customer_number}") 
    db_customer = await crud.update_customer(db, customer_number, customer_data)
    if db_customer is None:
        logging.error(f"API: Update failed - Customer {customer_number} not found") 
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

# DELETE: Delete [cite: 151]
@router.delete("/{customer_number}", status_code=204)
async def delete_existing_customer(customer_number: int, db: Session = Depends(database.get_db)):
    logging.info(f"API: DELETE request for customer {customer_number}") 
    success = await crud.delete_customer(db, customer_number)
    if not success:
        logging.error(f"API: Delete failed - Customer {customer_number} not found") 
        raise HTTPException(status_code=404, detail="Customer not found")
    return None # 204 No Content doesn't return a body




# Individual Count Endpoints
@router.get("/count/customers")
async def read_customers_count(db: Session = Depends(database.get_db)):
    logging.info("API: Request received for /count/customers") 
    count = await crud.get_customers_count(db)
    return {"customers": count}

@router.get("/count/orders")
async def read_orders_count(db:Session = Depends(database.get_db)):
    logging.info("API: Request received for /count/orders") 
    count = await crud.get_orders_count(db)
    return {"orders": count}

@router.get("/count/products")
async def read_products_count(db: Session = Depends(database.get_db)):
    count = await crud.get_products_count(db)
    return {"products": count}

@router.get("/count/employees")
async def read_employees_count(db: Session = Depends(database.get_db)):
    count = await crud.get_employees_count(db)
    return {"employees": count}

@router.get("/count/offices")
async def read_offices_count(db: Session = Depends(database.get_db)):
    count = await crud.get_offices_count(db)
    return {"offices": count}

@router.get("/count/payments")
async def read_payments_count(db: Session = Depends(database.get_db)):
    count = await crud.get_payments_count(db)
    return {"payments": count}

@router.get("/count/orderdetails")
async def read_orderdetails_count(db: Session = Depends(database.get_db)):
    count = await crud.get_orderdetails_count(db)
    return {"orderdetails": count}

@router.get("/count/productlines")
async def read_productlines_count(db: Session = Depends(database.get_db)):
    count = await crud.get_productlines_count(db)
    return {"productlines": count}


