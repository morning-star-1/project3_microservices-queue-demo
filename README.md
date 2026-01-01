# Microservices Queue Demo

A minimal microservices demo for asynchronous job processing using Flask, RabbitMQ, and a worker that can crash before ACK to show fault tolerance.

## Architecture
- API service publishes jobs to RabbitMQ.
- Worker service consumes and processes jobs.
- RabbitMQ provides durability and re-delivery.

## Quickstart
### Prerequisites
- Docker Desktop

### Run locally
```bash
docker compose up --build
```

Submit a job:
```bash
curl -X POST http://localhost:8080/jobs \
  -H "Content-Type: application/json" \
  -d '{"n":2}'
```

RabbitMQ UI: `http://localhost:15672` (guest/guest).

## Configuration
Environment variables are defined in `docker-compose.yml`:
- `RABBIT_URL`
- `QUEUE_NAME`
- `CRASH_PROB`

## Tests
```bash
python -m unittest discover -s tests
```
