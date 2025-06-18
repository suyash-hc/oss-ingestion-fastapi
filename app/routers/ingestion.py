from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from http import HTTPStatus
from app.logger import logger
from app.services.kafka import KafkaService
from typing import Dict, Any

router = APIRouter(tags=["ingestion"])
kafka_service = KafkaService()

@router.get("/health")
async def health():
    """Health check endpoint"""
    logger.info("Health check endpoint called")
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={"status": "ok"}
    )

@router.post("/ingest")
async def ingest_data(
    data: Dict[str, Any] = Body(...),
    topic: str = None
):
    """
    Ingest JSON data and send it to Kafka. If the data contains a 'media' field,
    it will be automatically base64 encoded before sending to Kafka.
    
    Args:
        data: The JSON data to ingest (media field will be base64 encoded if present)
        topic: Optional Kafka topic (defaults to configured default topic)
    
    Returns:
        JSON response with ingestion status
    """
    logger.info(f"Data ingestion request received")
    
    if not topic:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Topic name is required"
        )
    
    # Send to Kafka
    try:
        await kafka_service.send_to_kafka(topic, data)
    except ValueError as ve:
        # Handle invalid topic name errors
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        logger.error(f"Error sending to Kafka: {str(e)}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to send data to Kafka"
        )
    
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={
            "status": "Data sent to Kafka",
            "topic": topic,
            "data_size": len(str(data)),
            "media_encoded": "media" in data
        }
    )
