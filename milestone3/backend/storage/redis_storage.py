import redis
import json
from config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

TICKET_LIST_KEY = "processed_tickets"


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