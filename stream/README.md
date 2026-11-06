# Stream runbook

Install `pika` from requirements. Start a local RabbitMQ service or set `RABBITMQ_URL` in your local environment. Never paste a hosted broker URL into this repository.

1. In three terminals run `python stream/driver.py Ravi bangalore.koramangala.*`, `python stream/driver.py Arjun bangalore.*.ride`, and `python stream/driver.py Control bangalore.#`.
2. In another terminal run `python stream/dispatcher.py` for two minutes.
3. Save console evidence and stop all four processes. Private auto-delete queues disappear when drivers disconnect.
4. Every tenth event intentionally omits `zone`; the key uses `missing` so the dispatcher can still publish it. Drivers NACK it without requeue. Other valid events receive ACKs.

With `auto_ack=False`, a broker retains an unacknowledged delivery. If the consumer connection closes, RabbitMQ can requeue and redeliver it. A permanently malformed message with `requeue=True` can loop repeatedly; use dead-lettering or reject without requeue for poison messages.

