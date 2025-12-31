import json
import os
import time
import uuid

from flask import Flask, request, jsonify
import pika

RABBIT_URL = os.environ["RABBIT_URL"]
QUEUE = os.environ.get("QUEUE_NAME", "jobs")

app = Flask(__name__)

def get_channel():
    params = pika.URLParameters(RABBIT_URL)
    conn = pika.BlockingConnection(params)
    ch = conn.channel()
    ch.queue_declare(queue=QUEUE, durable=True)
    return conn, ch

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/jobs")
def create_job():
    data = request.get_json(force=True, silent=True) or {}
    job_id = str(uuid.uuid4())

    msg = {
        "jobId": job_id,
        "ts": time.time(),
        "data": data
    }

    conn, ch = get_channel()
    ch.basic_publish(
        exchange="",
        routing_key=QUEUE,
        body=json.dumps(msg).encode("utf-8"),
        properties=pika.BasicProperties(
            delivery_mode=2  # persistent message
        )
    )
    conn.close()

    # API returns immediately (async processing)
    return jsonify({"jobId": job_id, "enqueued": True}), 202

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
