from __future__ import annotations
import json, os, random, time
from datetime import datetime, timezone
import pika

EXCHANGE = "rapido-dispatch"
CITIES = {"bangalore": ["koramangala", "indiranagar", "whitefield"], "chennai": ["tnagar", "velachery"]}
TYPES = ["ride", "food"]

def connect():
    url = os.getenv("RABBITMQ_URL", "").strip()
    params = pika.URLParameters(url) if url else pika.ConnectionParameters("localhost")
    return pika.BlockingConnection(params)

def main():
    conn = connect(); ch = conn.channel()
    ch.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=True)
    count = 0
    try:
        while True:
            count += 1
            city = random.choice(list(CITIES)); zone = random.choice(CITIES[city]); kind = random.choice(TYPES)
            payload = {"id": f"REQ-{count:06d}", "city": city, "zone": zone, "type": kind,
                       "ts": datetime.now(timezone.utc).isoformat()}
            if count % 10 == 0:
                payload.pop("zone") # intentionally invalid test event
            key = f"{payload['city']}.{payload.get('zone', 'missing')}.{payload['type']}"
            ch.basic_publish(exchange=EXCHANGE, routing_key=key,
                body=json.dumps(payload), properties=pika.BasicProperties(delivery_mode=2, content_type="application/json"))
            print(f"sent {key}: {payload}", flush=True)
            time.sleep(2)
    except KeyboardInterrupt:
        pass
    finally:
        conn.close()
if __name__ == "__main__": main()

