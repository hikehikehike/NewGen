## 📌 Project Description
This is an API server built with **FastAPI**, using **PostgreSQL** and **SQLAlchemy**.  
The project is fully containerized with **Docker** and ready for deployment.

## ⚡ Quick Start

### 1️⃣ Clone the Repository
```bash
git clone git@github.com:hikehikehike/NewGen.git
cd NewGen
```

### 2️⃣ Ensure Docker is Installed
Check if Docker is installed:
```bash
docker --version
```
If not, download it from the [official website](https://www.docker.com/).

### 3️⃣ Build and Start the Containers

```bash
docker-compose up --build
```
This will:
* 	Build the necessary images.
* 	Start the FastAPI application.
* 	Start a PostgreSQL database.

### 4️⃣ Access the API
Once running, open:

http://127.0.0.1:8000/docs

This opens the FastAPI Swagger documentation.

### 5️⃣ Stop the Containers
To stop the containers, use:

```bash
docker-compose down
```
