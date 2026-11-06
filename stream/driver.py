from __future__ import annotations
import json, os, sys
import pika
from dispatcher import EXCHANGE, connect

def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: python driver.py NAME PATTERN")
    name, pattern = sys.argv[1:]
    conn = connect(); ch = conn.channel()
    ch.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=True)
    q = ch.queue_declare(queue="", exclusive=True, auto_delete=True).method.queue
    ch.queue_bind(exchange=EXCHANGE, queue=q, routing_key=pattern)
    ch.basic_qos(prefetch_count=1)
    print(f"{name} listening as {q} for {pattern}", flush=True)
    def handle(channel, method, props, body):
        try:
            msg = json.loads(body)
            if "zone" not in msg:
                channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                print(f"{name} discarded malformed {msg.get('id')}: missing zone", flush=True)
                return
            print(f"{name} received {method.routing_key}: {msg}", flush=True)
            channel.basic_ack(delivery_tag=method.delivery_tag)
        except (ValueError, TypeError) as exc:
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            print(f"{name} discarded invalid JSON: {exc}", flush=True)
    ch.basic_consume(queue=q, on_message_callback=handle, auto_ack=False)
    try: ch.start_consuming()
    except KeyboardInterrupt: ch.stop_consuming()
    finally: conn.close()
if __name__ == "__main__": main()

