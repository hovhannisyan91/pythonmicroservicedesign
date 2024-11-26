from Database.models import EmployeeDB, CustomerDB, ProductDB
from Database.schema import Employee, EmployeeCreate
from Database.database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException

app = FastAPI(title="FastAPI, Docker, and Traefik")

# GET Request - Retrieve an employee by ID
@app.get("/employees/{employee_id}", response_model=Employee)
async def get_employee(employee_id: int, db: Session = Depends(get_db)):
    """
    Retrieve an employee by their unique ID.

    **Parameters:**
    
    - `employee_id (int):` The unique identifier of the employee.
    - `db (Session, optional):` Database session provided by dependency injection.

    **Returns:**
        - `Employee:` The employee's details.

    **Raises:**

        - `HTTPException:` If the employee is not found, raises a 404 error.
    """
    employee = db.query(EmployeeDB).filter(EmployeeDB.employee_id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

# POST Request - Create a new employee
@app.post("/employees/", response_model=Employee)
async def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    """
    Create a new employee.

    **Parameters:**
    
    - `employee (EmployeeCreate):` The employee data to create.
    - `db (Session, optional):` Database session provided by dependency injection.

    **Returns:**
        - `Employee:` The newly created employee's details.
    """
    db_employee = EmployeeDB(
        first_name=employee.first_name,
        last_name=employee.last_name,
        email=employee.email,
        salary=employee.salary
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
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
    """
    Update an existing employee's details.

    **Parameters:**
    
    - `employee_id (int):` The unique identifier of the employee to update.
    - `updated_employee (EmployeeCreate):` The new employee data.
    - `db (Session, optional):` Database session provided by dependency injection.

    **Returns:**
        - `Employee:` The updated employee's details.

    **Raises:**

        - `HTTPException:` If the employee is not found, raises a 404 error.
    """
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
    """
    Delete an employee by their unique ID.

    **Parameters:**
    
    - `employee_id (int):` The unique identifier of the employee to delete.
    - `db (Session, optional):` Database session provided by dependency injection.

    **Returns:**
        - `dict:` A message confirming successful deletion.

    **Raises:**

        - `HTTPException:` If the employee is not found, raises a 404 error.
    """
    employee = db.query(EmployeeDB).filter(EmployeeDB.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
    return {"message": "Employee deleted successfully"}