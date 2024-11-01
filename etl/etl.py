# Loading modules and packages
from models import *


# import time

# # Pause code execution for 10 seconds
# print("Pausing for 20 seconds...")
# time.sleep(60)
# print("Resuming execution.")


from database import engine, Base



from data_generator import (
    generate_customer,
    generate_product,
    generate_orders,
    generate_employee,
    generate_sales,
)
import pandas as pd
from loguru import logger
import random
# Declaring Constants

NUMBER_OF_TRANSACTIONS=5000
NUMBER_OF_EMPLOYEES=100
NUMBER_OF_CUSTOMERS=2000
NUMBER_OF_ORDERS=200

# Generating Employee Data

employees = pd.DataFrame([generate_employee(employee_id) for employee_id in range(NUMBER_OF_EMPLOYEES)])

logger.info('Employee Data')
logger.info(employees.head(1))

employees.to_csv('data/employees.csv',index=False)
logger.info(f'Employee Data is saved to csv: {employees.shape}')

#########
customers = pd.DataFrame([generate_customer(customer_id) for customer_id in range(NUMBER_OF_CUSTOMERS)])
logger.info('Customer Data')
logger.info(customers.head(1))

customers.to_csv('data/customers.csv',index=False)
logger.info(f'Customer Data is saved to csv: {customers.shape}')

#########
products = pd.DataFrame([generate_product(product_id) for product_id in range(1, 101)])

logger.info('Product Data')
logger.info(products.head(1))

products.to_csv('data/products.csv',index=False)
logger.info(f'Product Data is saved to csv: {products.shape}')

#########
order = pd.DataFrame([generate_orders(order_id) for order_id in range(NUMBER_OF_ORDERS)] )

logger.info('Orders Data')
logger.info(employees.head(1))

order.to_csv('data/orders.csv',index=False)
logger.info(f'Order  Data is saved to csv: {order.shape}')

# Generating Sales Data

sales = []


for transaction_id in range(1, NUMBER_OF_TRANSACTIONS + 1):
    # Assuming you have order, product, customer, and employee lists
    order_id = random.randint(1, len(order))
    product_id = random.randint(1, len(products))
    customer_id = random.randint(1, len(customers))
    employee_id = random.randint(1, len(employees))
    
    sale = generate_sales(transaction_id, order_id, product_id, customer_id, employee_id)
    sales.append(sale)

sales=pd.DataFrame(sales)

sales.to_csv('data/sales.csv',index=False)
logger.info(f'Sales  Data is saved to csv: {sales.shape}')



def load_csv_to_table(table_name, csv_path):
    """
    Load data from a CSV file into a database table.

    Args:
    - table_name: Name of the database table.
    - csv_path: Path to the CSV file containing data.

    Returns:
    - None
    """
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, con=engine, if_exists="append", index=False)
    logger.info(f'loading {table_name}')


import glob
from os import path


# Specify the path to the folder, using "*" to match all files
folder_path = "data/*.csv"

# Use glob to get a list of file paths in the specified folder
files = glob.glob(folder_path)
base_names = [path.splitext(path.basename(file))[0] for file in files]
# Print the list of files
for table in base_names:
    try:
        load_csv_to_table(table, path.join("data/", f"{table}.csv"))
    except Exception as e:
        print(f"Failed to ingest table {table}. Moving to the next!")

print("Tables are populated.")