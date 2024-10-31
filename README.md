# Dockerized ETL, PostgreSQL, and pgAdmin Setup

## Installation


Before getting started, ensure you have the following prerequisites installed:

1. Clone the repository:
   ```bash
   git clone https://github.com/hovhannisyan91/pythonmicroservicedesign.git
   ```

2. Build and start the Docker containers:
   ```bash
   docker-compose up --build
   ```

## Docker 

This repository sets up a Docker environment with three main services:

1. **PostgreSQL:** for data storage
2. **pgAdmin:** for database management and visualization
3. **ETL:** service for Extract, Transform, Load operations using Python

## Prerequisites

Before running this setup, ensure Docker and Docker Compose are installed on your system.


- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)


## DB

- Access pgAdmin for PostgreSQL management: [http://localhost:5050](http://localhost:5050)
    - username: admin@admin.com 
    - password: admin
    - When running for the first time, you must create a server. Configure it as shown in the below image (Password is blurred it should be `password`.)
    ![Server Setup](presentation/imgs/pgadmin_setup.png)

### Environment Variables

Create a `.env` file in the root directory to define your environment variables as below:

```env
# PostgreSQL configuration
DB_USER=<your_database_user>
DB_PASSWORD=<your_database_password>
DB_NAME=<your_database_name>

# pgAdmin configuration
PGADMIN_EMAIL=<your_pgadmin_email>
PGADMIN_PASSWORD=<your_pgadmin_password>
```



## ETL

### Schema Design

We will try to create below schema:

![Star Schema](presentation/imgs/star_schema.png)

### ETL

In `models.py`, we have used `sqlalchemy` package, which allows map python objects with SQL objects.

By running `etl.py` following objects will be created:
    - sql tables 
    - the data sets will store in `data\` folder
    - the csv files will be loaded into DB

