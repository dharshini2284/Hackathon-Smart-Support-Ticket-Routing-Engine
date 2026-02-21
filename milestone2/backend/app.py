from fastapi import FastAPI
from pydantic import BaseModel
import uuid
from redis_queue import push_ticket
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
from typing import List
import csv
import io
from redis_queue import set_ticket_status,get_ticket_status

app = FastAPI(title="Smart Support Milestone 2")


class Ticket(BaseModel):
    text: str


@app.post("/tickets", status_code=202)
async def submit_ticket(ticket: Ticket):
    ticket_id = str(uuid.uuid4())

    payload = {
        "id": ticket_id,
        "text": ticket.text
    }

    # Save initial state
    set_ticket_status(ticket_id, {
        "status": "processing",
        "category": None,
        "urgency_score": None
    })

    push_ticket(payload)

    return {
        "ticket_id": ticket_id,
        "status": "accepted"
    }

@app.get("/tickets/{ticket_id}")
def get_status(ticket_id: str):
    data = get_ticket_status(ticket_id)
    if not data:
        return {"error": "Ticket not found"}
    return data

@app.post("/upload-csv", status_code=202)
async def upload_csv(file: UploadFile = File(...)):
    content = await file.read()
    decoded = content.decode("utf-8")

    csv_reader = csv.DictReader(io.StringIO(decoded))

    ticket_ids = []

    for row in csv_reader:
        ticket_id = str(uuid.uuid4())

        payload = {
            "id": ticket_id,
            "text": row["text"]
        }

        set_ticket_status(ticket_id, {
            "status": "processing",
            "category": None,
            "urgency_score": None
        })

        push_ticket(payload)
        ticket_ids.append(ticket_id)

    return {
        "message": "CSV accepted",
        "ticket_ids": ticket_ids
    }

@app.post("/tickets/bulk", status_code=202)
async def submit_bulk_tickets(tickets: List[str]):
    ticket_ids = []

    for text in tickets:
        ticket_id = str(uuid.uuid4())

        payload = {
            "id": ticket_id,
            "text": text
        }

        set_ticket_status(ticket_id, {
            "status": "processing",
            "category": None,
            "urgency_score": None
        })

        push_ticket(payload)
        ticket_ids.append(ticket_id)

    return {
        "message": "Tickets accepted",
        "ticket_ids": ticket_ids
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For hackathon demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)