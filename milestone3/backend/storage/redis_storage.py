import json
import redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379

TICKET_LIST_KEY = "processed_tickets"

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)


def store_ticket(ticket: dict):
    """
    Push processed ticket into Redis list.
    """
    redis_client.lpush(
        TICKET_LIST_KEY,
        json.dumps(ticket)
    )


def get_all_tickets(limit: int = 100):
    """
    Retrieve latest processed tickets.
    """
    tickets = redis_client.lrange(
        TICKET_LIST_KEY,
        0,
        limit - 1
    )

    return [json.loads(t) for t in tickets]


def clear_tickets():
    redis_client.delete(TICKET_LIST_KEY)