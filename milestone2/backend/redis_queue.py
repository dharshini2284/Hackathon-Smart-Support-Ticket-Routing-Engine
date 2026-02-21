import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

QUEUE_NAME = "ticket_queue"


def push_ticket(ticket: dict):
    redis_client.rpush(QUEUE_NAME, json.dumps(ticket))


def pop_ticket():
    _, data = redis_client.blpop(QUEUE_NAME)
    return json.loads(data)


# NEW: Ticket Status Storage

def set_ticket_status(ticket_id: str, data: dict):
    redis_client.set(f"ticket:{ticket_id}", json.dumps(data))


def get_ticket_status(ticket_id: str):
    data = redis_client.get(f"ticket:{ticket_id}")
    if data:
        return json.loads(data)
    return None