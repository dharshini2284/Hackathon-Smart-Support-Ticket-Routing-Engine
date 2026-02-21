import heapq
import time
from typing import Dict, Any

priority_queue = []


def push_ticket(ticket: Dict[str, Any], urgent: bool):
    """
    Lower number = higher priority
    Urgent tickets get priority 0
    Normal tickets get priority 1
    """
    priority = 0 if urgent else 1
    timestamp = time.time()

    heapq.heappush(priority_queue, (priority, timestamp, ticket))


def pop_ticket():
    if priority_queue:
        return heapq.heappop(priority_queue)
    return None

def get_all_tickets():
    """
    Returns tickets sorted by priority and timestamp
    without modifying the heap.
    """
    return sorted(priority_queue)

def get_queue_state():
    return priority_queue