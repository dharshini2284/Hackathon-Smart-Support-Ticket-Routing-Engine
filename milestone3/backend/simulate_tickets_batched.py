# simulate_tickets_batched.py
import requests
from faker import Faker
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

fake = Faker()

API_URL = "http://localhost:8000/tickets"

NUM_TICKETS = 1000           # total tickets to send
BATCH_SIZE = 20              # number of tickets to send simultaneously
DUPLICATE_RATIO = 0.1        # 10% duplicates for testing deduplication

categories = ["Billing", "Technical", "Legal"]
urgencies = ["low", "medium", "high", "critical"]

def generate_ticket(i):
    """Generate a single ticket"""
    if random.random() < DUPLICATE_RATIO:
        # duplicate ticket for storm simulation
        return {
            "id": i + 1,
            "title": "Server outage in region X ASAP",
            "description": "Our servers in region X are down, need immediate attention.",
            "category": "Technical",
            "urgency": "critical",
            "created_at": str(fake.date_time_this_year())
        }
    return {
        "id": i + 1,
        "title": fake.sentence(nb_words=6),
        "description": fake.text(max_nb_chars=200),
        "category": random.choice(categories),
        "urgency": random.choice(urgencies),
        "created_at": str(fake.date_time_this_year())
    }

def send_ticket(ticket):
    try:
        response = requests.post(API_URL, json=ticket)
        if response.status_code in [200, 202]:
            return f"Ticket {ticket['id']} ✅"
        else:
            return f"Ticket {ticket['id']} ❌ ({response.status_code})"
    except Exception as e:
        return f"Ticket {ticket['id']} ❌ ({e})"

def main():
    tickets = [generate_ticket(i) for i in range(NUM_TICKETS)]

    # Send tickets in batches to simulate same-millisecond arrivals
    for i in range(0, NUM_TICKETS, BATCH_SIZE):
        batch = tickets[i:i+BATCH_SIZE]
        with ThreadPoolExecutor(max_workers=BATCH_SIZE) as executor:
            futures = [executor.submit(send_ticket, t) for t in batch]
            for future in as_completed(futures):
                print(future.result())

if __name__ == "__main__":
    main()