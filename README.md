# Jupyter Notebook Container Setup

This guide explains how to set up and run a Jupyter Notebook container using Docker and Docker Compose.

---

## Dockerfile

The `Dockerfile` defines the environment for the Jupyter Notebook container. Below is the content of the `Dockerfile`:

```dockerfile
# filepath: myapp/notebook/Dockerfile
FROM python:3.12-slim-bullseye

RUN apt-get update && apt-get install -y \
    build-essential libpq-dev libfreetype6-dev libpng-dev libjpeg-dev \
    libblas-dev liblapack-dev gfortran \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /notebook

# Copy requirements file and install dependencies
COPY requirements.txt requirements.txt 
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8888 for Jupyter Notebook
EXPOSE 8888

# Command to run the python file
# CMD ["python", "generate_predictions.py"]

CMD ["bash", "-c", "python generate_predictions.py & jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --NotebookApp.token=''"]
```



## Docker Compose File

This is the `docker-compose.yaml` file used to define and run the multi-container Docker applications.

```yaml


version: "3.8"

services:
  notebook:
    build:
      context: ./notebook
      dockerfile: Dockerfile
    ports:
      - "8888:8888"
    volumes:
      - ./notebook:/notebook
    container_name: jupyter_notebook
```

## Running the Notebook

1. **Build and Start the Container**:
   ```bash
   docker-compose up --build
   ```
2. **Access the Notebook:** Open your browser and navigate to:

  ```bash
  http://localhost:8888
  ```
3. **Stop the Container:**
  ```bash
  docker-compose down
  ```
