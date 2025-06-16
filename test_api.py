import asyncio
import httpx
import json

async def test_health():
    """Test health endpoint"""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/ingestion/health")
        print(f"Health Check Response: {response.status_code}")
        print(f"Response Body: {response.json()}")

async def test_ingest():
    """Test data ingestion endpoint"""
    test_data = {
        "message": "Test message",
        "timestamp": "2024-02-20T10:00:00Z",
        "metadata": {
            "source": "test",
            "version": "1.0"
        }
    }
    
    async with httpx.AsyncClient() as client:
        # Test with default topic
        response = await client.post(
            "http://localhost:8000/ingestion/ingest",
            json=test_data
        )
        print(f"\nDefault Topic Response: {response.status_code}")
        print(f"Response Body: {response.json()}")
        
        # Test with custom topic
        response = await client.post(
            "http://localhost:8000/ingestion/ingest?topic=test-topic",
            json=test_data
        )
        print(f"\nCustom Topic Response: {response.status_code}")
        print(f"Response Body: {response.json()}")

async def main():
    print("Testing API endpoints...")
    await test_health()
    await test_ingest()

if __name__ == "__main__":
    asyncio.run(main()) 