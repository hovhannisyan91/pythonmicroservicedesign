# Dockerized ETL, PostgreSQL, and pgAdmin Setup

## Presentation 

**Follow to [this](https://hovhannisyan91.github.io/pythonmicroservicedesign/) link.**

## Installation

Before getting started, ensure you have the following prerequisites installed:

1. Clone the repository:
   ```bash
   git clone https://github.com/hovhannisyan91/pythonmicroservicedesign.git
   ```
2. Switch to the `db-setup` branch
    ```bash
    git checkout db-setup
    ```
3. Build and start the Docker containers:
   ```bash
   docker-compose up --build
   ```

## Access the Application

After running `docker-compose up --build`, you can access each component of the application at the following URLs:

- **PgAdmin** (optional): [http://localhost:5050](http://localhost:5050)  
  A graphical tool for PostgreSQL, which allows you to view and manage the database. Login using the credentials set in the `.env` file:
  
  - **Email**: Value of `PGADMIN_EMAIL` in your `.env` file
  - **Password**: Value of `PGADMIN_PASSWORD` in your `.env` file

> Note: Ensure Docker is running, and all environment variables in `.env` are correctly configured before accessing these URLs.

## Project Structure

Here’s an overview of the project’s file structure:

```bash
.
├── LICENSE
├── README.md
├── .env                # Environment variables
├── docker-compose.yml  # Docker Compose configuration
├── etl                 # Streamlit frontend folder
│   ├── Dockerfile      # Dockerfile for Streamlit container
│   ├── __init__.py
│   ├── etl.py          # Streamlit main entry point
│   └── requirements.txt # etl related dependencies
```

## Docker 

This **branch** sets up a Docker environment with three main services:

1. **PostgreSQL:** for data storage
2. **pgAdmin:** for database management and visualization
3. **ETL:** service for Extract, Transform, Load operations using Python

### Prerequisites

Before running this setup, ensure Docker and Docker Compose are installed on your system.


- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)


## DB

- Access pgAdmin for PostgreSQL management: [http://localhost:5050](http://localhost:5050)
    - username: admin@admin.com 
    - password: admin
    - When running for the first time, you must create a server. Configure it as shown in the below image (Password is blurred it should be `password`.)
    ![Server Setup](docs/imgs/pgadmin_setup.png)

### Environment Variables

Create a `.env` file in the root directory to define your environment variables as below:

```env
# PostgreSQL configuration
DB_USER=<your_database_user>
DB_PASSWORD=<your_database_password>
DB_NAME=<your_database_name>

# pgAdmin configuration; SUPER USER
PGADMIN_EMAIL=admin@admin.com
PGADMIN_PASSWORD=admin
```



## ETL

### Schema Design

We will try to create below schema:

![Star Schema](docs/imgs/star_schema.png)

### ETL

In `models.py`, we have used `sqlalchemy` package, which allows map python objects with SQL objects.

By running `etl.py` following objects will be created:
    - sql tables 
    - the data sets will store in `data\` folder
    - the csv files will be loaded into DB

### Dockerfile

```Dockerfile
FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y \
    build-essential libpq-dev libfreetype6-dev libpng-dev libjpeg-dev \
    libblas-dev liblapack-dev gfortran \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /etl

# Copy requirements file and install dependencies
COPY requirements.txt . 
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 3000
EXPOSE 3000

# Command to run the python file
CMD ["python", "etl.py"]
```

