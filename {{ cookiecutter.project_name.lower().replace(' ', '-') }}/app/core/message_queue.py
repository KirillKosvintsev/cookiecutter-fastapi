import json
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List

import aio_pika
from aio_pika import Message, connect_robust
from aio_pika.abc import AbstractIncomingMessage

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer


class MessageQueue(ABC):
    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass

    @abstractmethod
    async def publish(self, topic: str, message: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    async def consume(self, topics: List[str], callback: Callable) -> None:
        pass


class RabbitMQQueue(MessageQueue):
    def __init__(self, url: str):
        self.url = url
        self.connection = None
        self.channel = None

    async def connect(self) -> None:
        self.connection = await connect_robust(self.url)
        self.channel = await self.connection.channel()

    async def close(self) -> None:
        if self.connection:
            await self.connection.close()

    async def publish(self, routing_key: str, message: Dict[str, Any]) -> None:
        if not self.channel:
            await self.connect()

        await self.channel.default_exchange.publish(
            Message(body=json.dumps(message).encode()),
            routing_key=routing_key
        )

    async def consume(self, queue_names: List[str],
                      callback: Callable) -> None:
        if not self.channel:
            await self.connect()

        for queue_name in queue_names:
            queue = await self.channel.declare_queue(queue_name, durable=True)

            async def process_message(message: AbstractIncomingMessage):
                async with message.process():
                    body = json.loads(message.body.decode())
                    await callback(body)

            await queue.consume(process_message)


class KafkaQueue(MessageQueue):
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self.producer = None
        self.consumer = None

    async def connect(self) -> None:
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers)
        await self.producer.start()

    async def close(self) -> None:
        if self.producer:
            await self.producer.stop()
        if self.consumer:
            await self.consumer.stop()

    async def publish(self, topic: str, message: Dict[str, Any]) -> None:
        if not self.producer:
            await self.connect()

        await self.producer.send_and_wait(topic, json.dumps(message).encode())

    async def consume(self, topics: List[str], callback: Callable) -> None:
        self.consumer = AIOKafkaConsumer(
            *topics,
            bootstrap_servers=self.bootstrap_servers,
            group_id="my-group"
        )
        await self.consumer.start()

        try:
            async for msg in self.consumer:
                body = json.loads(msg.value.decode())
                await callback(body)
        finally:
            await self.consumer.stop()


class MessageProcessor:
    def __init__(self, queue: MessageQueue):
        self.queue = queue

    async def process_messages(self, topics: List[str]):
        await self.queue.consume(topics, self.handle_message)

    async def handle_message(self, message: Dict[str, Any]):
        # Implement your message processing logic here
        print(f"Received message: {message}")


# Example usage
async def main():
    # RabbitMQ example
    rabbitmq_url = "amqp://guest:guest@localhost/"
    rabbitmq_queue = RabbitMQQueue(rabbitmq_url)

    await rabbitmq_queue.connect()
    await rabbitmq_queue.publish("test_queue", {"message": "Hello, RabbitMQ!"})

    rabbitmq_processor = MessageProcessor(rabbitmq_queue)
    await rabbitmq_processor.process_messages(["test_queue"])

    await rabbitmq_queue.close()

    # Kafka example
    kafka_bootstrap_servers = "localhost:9092"
    kafka_queue = KafkaQueue(kafka_bootstrap_servers)

    await kafka_queue.connect()
    await kafka_queue.publish("test_topic", {"message": "Hello, Kafka!"})

    kafka_processor = MessageProcessor(kafka_queue)
    await kafka_processor.process_messages(["test_topic"])

    await kafka_queue.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())