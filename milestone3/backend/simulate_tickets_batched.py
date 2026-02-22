# simulate_tickets_batched.py

import requests
from faker import Faker
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

fake = Faker()

API_URL = "http://localhost:8000/tickets"

NUM_TICKETS = 1000
BATCH_SIZE = 20
DUPLICATE_RATIO = 0.2  # Increase to test flood detection


def generate_ticket(i):
    """
    Generates payload matching FastAPI model:
    {
        "ticket_id": str,
        "text": str
    }
    """

    # Simulate duplicate storm
    if random.random() < DUPLICATE_RATIO:
        return {
            "ticket_id": str(i + 1),
            "text": "Server outage in region X. Production down ASAP."
        }

    # Normal random ticket
    return {
        "ticket_id": str(i + 1),
        "text": fake.text(max_nb_chars=200)
    }


def send_ticket(ticket):
    try:
        response = requests.post(API_URL, json=ticket)

        if response.status_code in [200, 202]:
            return f"Ticket {ticket['ticket_id']} ✅"
        else:
            return f"Ticket {ticket['ticket_id']} ❌ ({response.status_code})"

    except Exception as e:
        return f"Ticket {ticket['ticket_id']} ❌ ({e})"


def main():
    tickets = [generate_ticket(i) for i in range(NUM_TICKETS)]

    # Send in batches to simulate same-millisecond load
    for i in range(0, NUM_TICKETS, BATCH_SIZE):
        batch = tickets[i:i + BATCH_SIZE]

        with ThreadPoolExecutor(max_workers=BATCH_SIZE) as executor:
            futures = [executor.submit(send_ticket, t) for t in batch]

            for future in as_completed(futures):
                print(future.result())


if __name__ == "__main__":
    main()