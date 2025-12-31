# Architecture

## Overview
- API service publishes jobs to RabbitMQ
- Worker service consumes jobs asynchronously
- RabbitMQ provides durability and re-delivery

## Data flow
Client -> API -> RabbitMQ -> Worker

## Key decisions
- Manual ACK to demonstrate at-least-once delivery
- Docker Compose for a reproducible dev setup
