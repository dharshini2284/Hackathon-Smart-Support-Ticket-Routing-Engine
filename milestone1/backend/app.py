from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import time
from fastapi.middleware.cors import CORSMiddleware
from model import classify_ticket, detect_urgency
from queue_manager import push_ticket, pop_ticket, get_queue_state, get_all_tickets

app = FastAPI(title="Smart Support MVR")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Ticket(BaseModel):
    text: str


@app.post("/tickets")
def submit_ticket(ticket: Ticket):
    ticket_id = str(uuid.uuid4())
    timestamp = time.time()

    category = classify_ticket(ticket.text)
    urgent = detect_urgency(ticket.text)

    ticket_payload = {
        "id": ticket_id,
        "text": ticket.text,
        "category": category,
        "urgent": urgent,
        "timestamp": timestamp
    }

    push_ticket(ticket_payload, urgent)

    return {
        "ticket_id": ticket_id,
        "category": category,
        "urgent": urgent,
        "status": "queued"
    }

@app.get("/tickets")
def view_all_tickets():
    tickets = get_all_tickets()
    
    result = []
    for priority, timestamp, ticket in tickets:
        result.append({
            "priority": priority,
            "ticket": ticket
        })

    return {
        "total": len(result),
        "tickets": result
    }
    
@app.get("/next-ticket")
def get_next_ticket():
    item = pop_ticket()
    if not item:
        return {"message": "Queue is empty"}

    priority, timestamp, ticket = item
    return ticket


@app.get("/queue")
def view_queue():
    return {"queue_size": len(get_queue_state())}