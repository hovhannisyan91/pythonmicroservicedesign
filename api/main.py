from api.Database.models import EmployeeDB, CustomerDB, ProductDB
from api.Database.schema import Employee, EmployeeCreate
from api.Database.database import get_db



from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from typing import Dict

app = FastAPI(title="FastAPI, Docker, and Traefik")

# GET Request - Retrieve an employee by ID
@app.get("/employees/{employee_id}", response_model=Employee)
async def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(EmployeeDB).filter(EmployeeDB.employee_id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

# POST Request - Create a new employee
@app.post("/employees/", response_model=Employee)
async def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    # Create an instance of the EmployeeDB model using the data from the EmployeeCreate schema
    db_employee = EmployeeDB(
        first_name=employee.first_name,
        last_name=employee.last_name,
        email=employee.email,
        salary=employee.salary
    )
    
    # Add the employee to the database session
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)  # Refresh to get the updated employee with its auto-generated employee_id
    
    # Convert the ORM model (EmployeeDB) to a Pydantic model (Employee)
    return Employee(
        employee_id=db_employee.employee_id,
        first_name=db_employee.first_name,
        last_name=db_employee.last_name,
        email=db_employee.email,
        salary=db_employee.salary
    )

# PUT Request - Update an existing employee
@app.put("/employees/{employee_id}", response_model=Employee)
async def update_employee(employee_id: int, updated_employee: EmployeeCreate, db: Session = Depends(get_db)):
    employee = db.query(EmployeeDB).filter(EmployeeDB.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    for key, value in updated_employee.dict().items():
        setattr(employee, key, value)
    db.commit()
    db.refresh(employee)
    return employee

# DELETE Request - Delete an employee by ID
@app.delete("/employees/{employee_id}")
async def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(EmployeeDB).filter(EmployeeDB.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
    return {"message": "Employee deleted successfully"}
