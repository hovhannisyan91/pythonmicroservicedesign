from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()

# Database Models
class EmployeeDB(Base):
    __tablename__ = "employees"
    employee_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    salary = Column(Integer)

class CustomerDB(Base):
    __tablename__ = "customers"
    customer_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    customer_name = Column(String, index=True)
    address = Column(String)
    city = Column(String)
    zip_code = Column(String)

class ProductDB(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    product_name = Column(String, index=True)
    price = Column(Float)
    description = Column(String)
    category = Column(String)