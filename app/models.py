from sqlalchemy import String, Integer, Numeric,ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base
from decimal import Decimal
from sqlalchemy import Date, Text

class Customer(Base):
    """SQLAlchemy model for the customers table """
    __tablename__ = "customers"

    # Match the image columns exactly 
    customerNumber: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customerName: Mapped[str] = mapped_column(String(50), nullable=False)
    contactLastName: Mapped[str] = mapped_column(String(50), nullable=False)
    contactFirstName: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)
    addressLine1: Mapped[str] = mapped_column(String(50), nullable=False)
    addressLine2: Mapped[str] = mapped_column(String(50), nullable=True) # Optional in many schemas
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    state: Mapped[str] = mapped_column(String(50), nullable=True)
    postalCode: Mapped[str] = mapped_column(String(15), nullable=True)
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    salesRepEmployeeNumber: Mapped[int] = mapped_column(Integer, nullable=True)
    creditLimit: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)







# --- Existing Customer Model here ---


class Order(Base):
    __tablename__ = "orders"
    
    orderNumber: Mapped[int] = mapped_column(Integer, primary_key=True)
    orderDate: Mapped[str] = mapped_column(Date, nullable=False)
    requiredDate: Mapped[str] = mapped_column(Date, nullable=False)
    shippedDate: Mapped[str] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(15), nullable=False)
    comments: Mapped[str] = mapped_column(Text, nullable=True)
    customerNumber: Mapped[int] = mapped_column(Integer, ForeignKey("customers.customerNumber"), nullable=False)
  

class Product(Base):
    
    __tablename__ = "products"
    productCode: Mapped[str] = mapped_column(String(15), primary_key=True)
    productName: Mapped[str] = mapped_column(String(70), nullable=False)
    productLine: Mapped[str] = mapped_column(String(50), ForeignKey("productlines.productLine"), nullable=False)
    productScale: Mapped[str] = mapped_column(String(10), nullable=False)
    productVendor: Mapped[str] = mapped_column(String(50), nullable=False)
    productDescription: Mapped[str] = mapped_column(String, nullable=False)
    quantityInStock: Mapped[int] = mapped_column(Integer, nullable=False)
    buyPrice: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    MSRP: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

class Employee(Base):
    __tablename__ = "employees"
    
    employeeNumber: Mapped[int] = mapped_column(Integer, primary_key=True)
    lastName: Mapped[str] = mapped_column(String(50), nullable=False)
    firstName: Mapped[str] = mapped_column(String(50), nullable=False)
    extension: Mapped[str] = mapped_column(String(10), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    officeCode: Mapped[str] = mapped_column(String(10), ForeignKey("offices.officeCode"), nullable=False)
    reportsTo: Mapped[int] = mapped_column(Integer, ForeignKey("employees.employeeNumber"), nullable=True)
    jobTitle: Mapped[str] = mapped_column(String(50), nullable=False)

class Office(Base):
    __tablename__ = "offices"
    officeCode: Mapped[str] = mapped_column(String(10), primary_key=True)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)
    addressLine1: Mapped[str] = mapped_column(String(50), nullable=False)
    addressLine2: Mapped[str] = mapped_column(String(50), nullable=True)
    state: Mapped[str] = mapped_column(String(50), nullable=True)
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    postalCode: Mapped[str] = mapped_column(String(15), nullable=False)
    territory: Mapped[str] = mapped_column(String(10), nullable=False)

class Payment(Base):
    __tablename__ = "payments"

    # Composite Primary Key
    customerNumber: Mapped[int] = mapped_column(Integer, ForeignKey("customers.customerNumber"), primary_key=True)
    checkNumber: Mapped[str] = mapped_column(String(50), primary_key=True)

    paymentDate: Mapped[Date] = mapped_column(Date, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

class OrderDetail(Base):
    __tablename__ = "orderdetails"

    # Composite Primary Key: orderNumber + productCode
    orderNumber: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("orders.orderNumber"), 
        primary_key=True
    )
    productCode: Mapped[str] = mapped_column(
        String(15), 
        ForeignKey("products.productCode"), 
        primary_key=True
    )

    quantityOrdered: Mapped[int] = mapped_column(Integer, nullable=False)
    priceEach: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    orderLineNumber: Mapped[int] = mapped_column(SmallInteger, nullable=False)


class ProductLine(Base):
    __tablename__ = "productlines"
    productLine: Mapped[str] = mapped_column(String(50), primary_key=True)
    textDescription: Mapped[str] = mapped_column(String(4000), nullable=True)
    htmlDescription: Mapped[str] = mapped_column(String, nullable=True)
    image: Mapped[bytes] = mapped_column(nullable=True)