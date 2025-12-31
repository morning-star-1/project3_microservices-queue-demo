import json
import os
import random
import time

import pika

RABBIT_URL = os.environ["RABBIT_URL"]
QUEUE = os.environ.get("QUEUE_NAME", "jobs")
CRASH_PROB = float(os.environ.get("CRASH_PROB", "0.2"))

params = pika.URLParameters(RABBIT_URL)

def on_message(ch, method, properties, body: bytes):
    msg = json.loads(body.decode("utf-8"))
    job_id = msg.get("jobId")
    n = (msg.get("data") or {}).get("n", 1)

    print(f"[worker] start job={job_id} n={n}")
    time.sleep(float(n))

    # Fault tolerance demo: crash BEFORE ACK sometimes -> message requeued/redelivered
    if random.random() < CRASH_PROB:
        print(f"[worker] simulated crash job={job_id} (no ack)")
        os._exit(1)

    print(f"[worker] done job={job_id} -> ACK")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def run():
    while True:
        try:
            conn = pika.BlockingConnection(params)
            ch = conn.channel()
            ch.queue_declare(queue=QUEUE, durable=True)

            # Fair dispatch (each worker grabs 1 job at a time)
            ch.basic_qos(prefetch_count=1)

            ch.basic_consume(queue=QUEUE, on_message_callback=on_message)
            print("[worker] waiting for jobs...")
            ch.start_consuming()
        except Exception as e:
            print("[worker] error, retrying:", e)
            time.sleep(2)

if __name__ == "__main__":
    run()
