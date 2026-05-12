
from fastapi import FastAPI
from .Router import customer_router, office_router  , product_router, productline_router,employee_router, order_router, orderdetail_router,payment_router
from app.database import engine, Base
import logging

# Initialize FastAPI with the metadata from the guide
app = FastAPI(title='ClassicModels API', version='2.0') 

# Register the Customer router with its prefix and tag
app.include_router(customer_router.router, prefix='/customers', tags=['Customers']) 
app.include_router( product_router.router, prefix='/products', tags=['Products'] )
app.include_router( productline_router.router, prefix='/productlines', tags=['ProductLines'] )
app.include_router( office_router.router, prefix='/offices', tags=['Offices'] )
app.include_router( employee_router.router, prefix='/employees', tags=['Employees'] )
app.include_router( order_router.router, prefix='/orders', tags=['Orders'] )
app.include_router( orderdetail_router.router, prefix='/orderdetails', tags=['OrderDetails'] )
app.include_router( payment_router.router, prefix='/payments', tags=['Payments'] )
@app.get('/')
def root():
    logging.info('Root endpoint accessed') 
    return {'message': 'ClassicModels API is running!'} 