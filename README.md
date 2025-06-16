# OSS Ingestion Service

A FastAPI-based microservice built with Gin framework for handling image ingestion and Kafka integration.

## Prerequisites
- Docker and Docker Compose
- Git
- curl (for testing)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create the `.env` File
Copy the `.env.example` file and update the values in the `.env` file:
```bash
cp .env.example .env
```
### 3.Start all services:
   ```bash
   docker-compose up -d
   ```
This will start:
- The application server (port 8080)
- Kafka (ports 9092, 29092)
- Zookeeper (port 2181)
- Kafka UI (port 8082)

## API Documentation

Access the Swagger UI at: `http://localhost:8080/ingestion/docs`

## API Endpoints

### Health Check
- `GET /ingestion/health`
  - Returns service health status
  - Response: `{"status": "ok"}`

### Image Ingestion
- `POST /ingestion/ingest`
  - Accepts image files
  - Query Parameters:
    - `topic` (optional): Kafka topic name

## Kafka UI
Access Kafka UI at: `http://localhost:8082`

