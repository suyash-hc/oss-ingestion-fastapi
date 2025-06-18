from typing import Optional, Dict, Any
import aiokafka
import json
import re
from app.config import settings
from app.logger import logger
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
import base64

class KafkaService:
    def __init__(self):
        self.bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS
        self.producer: Optional[aiokafka.AIOKafkaProducer] = None
        self.admin_client: Optional[KafkaAdminClient] = None
    
    def _validate_topic_name(self, topic: str) -> None:
        """Validate Kafka topic name according to Kafka naming conventions"""
        if not topic:
            raise ValueError("Topic name cannot be empty")
        
        # Kafka topic naming rules:
        # - Only ASCII alphanumerics, dots, underscores, and hyphens allowed
        # - Cannot be empty
        # - Cannot be longer than 249 characters
        if len(topic) > 249:
            raise ValueError("Topic name cannot be longer than 249 characters")
            
        if not re.match(r'^[a-zA-Z0-9._-]+$', topic):
            raise ValueError(
                "Topic name can only contain ASCII alphanumerics, dots (.), "
                "underscores (_), and hyphens (-)"
            )
    
    async def _ensure_producer(self) -> aiokafka.AIOKafkaProducer:
        """Ensure Kafka producer is initialized"""
        if self.producer is None:
            self.producer = aiokafka.AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                client_id=settings.KAFKA_CLIENT_ID,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None
            )
            await self.producer.start()
        return self.producer
    
    def _get_admin_client(self) -> KafkaAdminClient:
        """Get or create Kafka admin client"""
        if self.admin_client is None:
            self.admin_client = KafkaAdminClient(
                bootstrap_servers=self.bootstrap_servers
            )
        return self.admin_client

    def _create_topic_if_not_exists(self, topic: str) -> None:
        """Create Kafka topic if it doesn't exist"""
        try:
            # Validate topic name first
            self._validate_topic_name(topic)
            
            admin_client = self._get_admin_client()
            topic_list = [NewTopic(name=topic, num_partitions=1, replication_factor=1)]
            admin_client.create_topics(topic_list)
            logger.info(f"Created Kafka topic: {topic}")
        except TopicAlreadyExistsError:
            logger.info(f"Topic {topic} already exists")
        except ValueError as ve:
            logger.error(f"Invalid topic name {topic}: {str(ve)}")
            raise
        except Exception as e:
            logger.error(f"Error creating Kafka topic {topic}: {str(e)}")
            raise
    
    async def send_to_kafka(self, topic: str, data: Dict[str, Any]) -> None:
        """
        Send data to Kafka topic. If data contains a 'media' field, it will be base64 encoded.
        
        Args:
            topic: Kafka topic name
            data: Data to send (media field will be base64 encoded if present)
        """
        try:
            # Validate topic name first
            self._validate_topic_name(topic)
            
            # Create topic if it doesn't exist
            self._create_topic_if_not_exists(topic)
            
            # Process data to encode media field if present
            processed_data = data.copy()
            if 'media' in processed_data:
                media_data = processed_data['media']
                if isinstance(media_data, str):
                    # If media is already a string, encode it
                    processed_data['media'] = base64.b64encode(media_data.encode('utf-8')).decode('utf-8')
                else:
                    # If media is bytes or other format, encode it directly
                    processed_data['media'] = base64.b64encode(str(media_data).encode('utf-8')).decode('utf-8')
            
            # Get producer and send message
            producer = await self._ensure_producer()
            await producer.send_and_wait(topic, value=processed_data)
            logger.info(f"Successfully sent data to topic {topic}")
        except ValueError as ve:
            logger.error(f"Invalid topic name {topic}: {str(ve)}")
            raise
        except Exception as e:
            logger.error(f"Error sending to Kafka: {str(e)}")
            raise
    
    async def close(self):
        """Close the Kafka producer and admin client"""
        if self.producer:
            await self.producer.stop()
            self.producer = None
            
        if self.admin_client:
            self.admin_client.close()
            self.admin_client = None 

# Create singleton instance
kafka_service = KafkaService() 