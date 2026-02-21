from redis_queue import pop_ticket
from transformer_model import classify_ticket, get_urgency_score
from webhook import trigger_alert
from redis_queue import set_ticket_status
import time


def process_ticket(ticket):
    ticket_id = ticket["id"]
    text = ticket["text"]

    start = time.time()

    category = classify_ticket(text)
    urgency_score = get_urgency_score(text)

    latency = time.time() - start

    webhook_triggered = False

    if urgency_score > 0.8:
        trigger_alert(ticket, urgency_score)
        webhook_triggered = True

    set_ticket_status(ticket_id, {
        "status": "completed",
        "ticket_text": text,
        "category": category,
        "urgency_score": urgency_score,
        "latency_ms": round(latency * 1000, 2),
        "webhook_triggered": webhook_triggered
    })

if __name__ == "__main__":
    print("Worker started...")
    while True:
        ticket = pop_ticket()
        process_ticket(ticket)