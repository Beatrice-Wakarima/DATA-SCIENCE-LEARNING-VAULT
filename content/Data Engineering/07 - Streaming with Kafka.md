---
title: Streaming with Kafka
tags: [data-engineering, kafka, streaming, real-time]
created: 2026-05-20
up:: [[Data Engineering MOC]]
---

# 🌊 Streaming with Kafka

> Apache Kafka is the industry standard for real-time data streaming. It decouples producers and consumers, handles millions of events per second, and enables real-time analytics, fraud detection, and event-driven architectures.

---

## Batch vs Streaming

```
Batch Processing:              Stream Processing:
────────────────               ────────────────────
Process data hourly/daily      Process data as it arrives
Results available later        Results available immediately
Simpler to build               More complex but real-time
Lower cost                     Higher infrastructure cost

Example: Daily sales report    Example: Fraud detection in <1s
```

---

## Kafka Core Concepts

```
Producer    → Application that sends messages to Kafka
Consumer    → Application that reads messages from Kafka
Topic       → Named channel for messages (like a table)
Partition   → Topic split for parallelism and ordering
Offset      → Position of a message in a partition
Broker      → Kafka server (node)
Cluster     → Group of Kafka brokers
Consumer Group → Set of consumers sharing topic load
Retention   → How long messages are kept (default: 7 days)
```

---

## Kafka Architecture

```
┌──────────────┐                    ┌──────────────────┐
│   Producer   │  → messages →      │   Kafka Cluster  │
│  (Python app)│                    │                  │
│  (FastAPI)   │    Topic:          │  Topic: transactions
│  (IoT sensor)│    transactions    │  ┌─────────────┐ │
└──────────────┘                    │  │ Partition 0 │ │
                                    │  │ Partition 1 │ │
┌──────────────┐  ← messages ←      │  │ Partition 2 │ │
│   Consumer   │                    │  └─────────────┘ │
│  (Pipeline)  │                    └──────────────────┘
│  (ML Model)  │
│  (Dashboard) │
└──────────────┘
```

---

## Kafka with Docker Compose

```yaml
# docker-compose.kafka.yml
version: "3.8"

services:

  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    container_name: zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    networks:
      - kafka-net

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    container_name: kafka
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"
      KAFKA_RETENTION_MS: 604800000       # 7 days
    networks:
      - kafka-net

  kafka-ui:
    image: provectuslabs/kafka-ui:latest
    container_name: kafka-ui
    ports:
      - "8090:8080"
    environment:
      KAFKA_CLUSTERS_0_NAME: local
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka:9092
    depends_on:
      - kafka
    networks:
      - kafka-net

networks:
  kafka-net:
```

```bash
docker compose -f docker-compose.kafka.yml up -d
# Kafka UI: http://localhost:8090
```

---

## Python Kafka Producer

```python
# src/streaming/producer.py
from confluent_kafka import Producer
import json
import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)

class KafkaProducer:
    """Produce messages to Kafka topics"""

    def __init__(self, bootstrap_servers: str = "localhost:9092"):
        self.producer = Producer({
            "bootstrap.servers": bootstrap_servers,
            "acks": "all",                  # Wait for all replicas
            "retries": 3,
            "retry.backoff.ms": 300,
            "compression.type": "snappy",   # Compress messages
            "linger.ms": 5,                 # Batch up to 5ms
            "batch.size": 65536             # 64KB batches
        })

    def _delivery_report(self, err, msg):
        """Callback after message delivery"""
        if err:
            logger.error(f"Message delivery failed: {err}")
        else:
            logger.debug(
                f"Delivered to {msg.topic()}[{msg.partition()}] "
                f"@ offset {msg.offset()}"
            )

    def produce(self, topic: str, value: Dict,
                key: str = None) -> None:
        """Send a single message"""
        # Add metadata
        value["_produced_at"] = datetime.now().isoformat()

        self.producer.produce(
            topic=topic,
            key=key.encode("utf-8") if key else None,
            value=json.dumps(value).encode("utf-8"),
            callback=self._delivery_report
        )
        self.producer.poll(0)       # Trigger delivery reports

    def produce_batch(self, topic: str,
                      messages: list, key_field: str = None) -> int:
        """Send a batch of messages"""
        sent = 0
        for msg in messages:
            key = str(msg.get(key_field)) if key_field else None
            self.produce(topic, msg, key=key)
            sent += 1

        self.producer.flush()       # Wait for all to be delivered
        logger.info(f"Produced {sent:,} messages to {topic}")
        return sent

    def close(self):
        self.producer.flush(timeout=10)


# Simulate bank transaction events
def simulate_bank_transactions(num_events: int = 100):
    """Simulate real-time bank transactions"""
    import random

    producer = KafkaProducer()

    customers = [101, 102, 103, 104, 105]
    transaction_types = ["deposit", "withdrawal", "transfer"]

    for i in range(num_events):
        event = {
            "transaction_id": f"TXN{i:06d}",
            "customer_id": random.choice(customers),
            "amount": round(random.uniform(100, 50000), 2),
            "type": random.choice(transaction_types),
            "currency": "KES",
            "timestamp": datetime.now().isoformat(),
            "channel": random.choice(["mobile", "atm", "branch"])
        }

        producer.produce(
            topic="bank.transactions",
            value=event,
            key=str(event["customer_id"])
        )

    producer.close()
    print(f"✅ Produced {num_events} transaction events")

if __name__ == "__main__":
    simulate_bank_transactions(1000)
```

---

## Python Kafka Consumer

```python
# src/streaming/consumer.py
from confluent_kafka import Consumer, KafkaException
import json
import logging
import pandas as pd
from datetime import datetime
from typing import Callable

logger = logging.getLogger(__name__)

class KafkaConsumer:
    """Consume and process messages from Kafka topics"""

    def __init__(self,
                 bootstrap_servers: str = "localhost:9092",
                 group_id: str = "bank-pipeline",
                 auto_offset_reset: str = "earliest"):
        self.consumer = Consumer({
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": auto_offset_reset,
            "enable.auto.commit": False,    # Manual commit for safety
            "max.poll.interval.ms": 300000  # 5 minute timeout
        })

    def consume(self, topics: list,
                processor: Callable,
                batch_size: int = 100,
                timeout: float = 1.0):
        """Consume messages and process in batches"""

        self.consumer.subscribe(topics)
        logger.info(f"Subscribed to: {topics}")

        batch = []
        total_processed = 0

        try:
            while True:
                msg = self.consumer.poll(timeout=timeout)

                if msg is None:
                    # No message — process any remaining batch
                    if batch:
                        processor(batch)
                        total_processed += len(batch)
                        self.consumer.commit()
                        batch = []
                    continue

                if msg.error():
                    if msg.error().code() == -191:  # End of partition
                        continue
                    raise KafkaException(msg.error())

                # Decode message
                try:
                    value = json.loads(msg.value().decode("utf-8"))
                    batch.append(value)
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to decode message: {e}")
                    continue

                # Process batch when full
                if len(batch) >= batch_size:
                    processor(batch)
                    total_processed += len(batch)
                    self.consumer.commit()      # Commit after processing
                    logger.info(f"Processed batch: {total_processed:,} total")
                    batch = []

        except KeyboardInterrupt:
            logger.info("Consumer stopped")
        finally:
            if batch:
                processor(batch)
                self.consumer.commit()
            self.consumer.close()
            logger.info(f"Total processed: {total_processed:,}")


# Real-time fraud detection processor
def detect_fraud(messages: list) -> None:
    """Process transaction batch — flag suspicious activity"""
    df = pd.DataFrame(messages)

    # Flag suspicious transactions
    df["is_suspicious"] = (
        (df["amount"] > 100000) |                   # Large amount
        (df["type"] == "withdrawal") & (df["amount"] > 50000) |
        (df.groupby("customer_id")["transaction_id"]
           .transform("count") > 10)                 # Too many in batch
    )

    suspicious = df[df["is_suspicious"]]
    if len(suspicious) > 0:
        logger.warning(
            f"🚨 {len(suspicious)} suspicious transactions detected!"
        )
        # Send alert, log to fraud table, etc.
        for _, txn in suspicious.iterrows():
            logger.warning(
                f"  TXN {txn['transaction_id']}: "
                f"KES {txn['amount']:,.0f} ({txn['type']})"
            )

    # Store to database
    from sqlalchemy import create_engine
    import os
    engine = create_engine(os.getenv("DB_URL"))
    df.to_sql("stream_transactions", engine,
              if_exists="append", index=False)


# Run consumer
if __name__ == "__main__":
    consumer = KafkaConsumer(group_id="fraud-detection")
    consumer.consume(
        topics=["bank.transactions"],
        processor=detect_fraud,
        batch_size=100
    )
```

---

## Topics and Partitions

```bash
# Create topics via Kafka CLI inside container
docker exec kafka kafka-topics \
  --create \
  --bootstrap-server localhost:9092 \
  --topic bank.transactions \
  --partitions 3 \
  --replication-factor 1

docker exec kafka kafka-topics \
  --create \
  --bootstrap-server localhost:9092 \
  --topic bank.fraud.alerts \
  --partitions 1 \
  --replication-factor 1

# List topics
docker exec kafka kafka-topics \
  --list --bootstrap-server localhost:9092

# Describe topic
docker exec kafka kafka-topics \
  --describe \
  --topic bank.transactions \
  --bootstrap-server localhost:9092

# Consume messages from terminal
docker exec kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic bank.transactions \
  --from-beginning
```

---

## Streaming Pipeline Architecture

```
Mobile App / ATM
        ↓ REST API
    FastAPI
        ↓ produce
  Kafka Topic: bank.transactions
        ↓ consume
  ┌─────────────────────────────┐
  │  Consumer Group: pipeline   │
  │                             │
  │  Consumer 1: Fraud Detection│
  │  Consumer 2: Analytics DB   │
  │  Consumer 3: Notifications  │
  └─────────────────────────────┘
        ↓
  PostgreSQL / Data Warehouse
        ↓
  Power BI Dashboard (near real-time)
```

---

## Quick Reference

```python
# Producer
from confluent_kafka import Producer
p = Producer({"bootstrap.servers": "localhost:9092"})
p.produce("topic", key="key", value=json.dumps(msg).encode())
p.flush()

# Consumer
from confluent_kafka import Consumer
c = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "my-group",
    "auto.offset.reset": "earliest"
})
c.subscribe(["topic"])
msg = c.poll(1.0)
value = json.loads(msg.value().decode())
c.commit()
c.close()

# Key Kafka concepts
Topic         → Named message stream
Partition     → Parallel subdivisions of a topic
Consumer Group → Load-balanced consumers
Offset        → Message position (committed after processing)
Retention     → How long messages are kept
```

---

## Previous | Next
← [[06 - Data Quality and Validation]] | → [[08 - End-to-End Pipeline Project]]
