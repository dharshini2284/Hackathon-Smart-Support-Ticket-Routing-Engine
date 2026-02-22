import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

from .queue.redis_client import RedisBroker
from .worker.orchestrator_worker import handle_ticket
from .orchestration.incident_manager import IncidentManager

# --------------------------------------------
# FastAPI App
# --------------------------------------------

app = FastAPI(title="AI Ticket Orchestrator")
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",  # your frontend URL
    "http://127.0.0.1:5173",
    # you can add more origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, etc.
    allow_headers=["*"],  # Authorization, Content-Type, etc.
)
# --------------------------------------------
# Broker + Incident Manager
# --------------------------------------------

broker = RedisBroker()
incident_manager = IncidentManager()

# --------------------------------------------
# Request Model
# --------------------------------------------

class TicketRequest(BaseModel):
    ticket_id: str
    text: str


# --------------------------------------------
# Startup Event
# --------------------------------------------

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(
        broker.start_worker(handle_ticket)
    )
    print("🚀 Worker started")


# --------------------------------------------
# Submit Ticket
# --------------------------------------------

@app.post("/tickets")
async def submit_ticket(ticket: TicketRequest):

    await broker.publish(ticket.dict())

    return {
        "message": "Ticket submitted",
        "ticket_id": ticket.ticket_id
    }


# --------------------------------------------
# Health Check
# --------------------------------------------

@app.get("/health")
async def health():
    return {"status": "OK"}


# --------------------------------------------
# Incident Status
# --------------------------------------------

@app.get("/incidents")  # plural to match requests
async def get_incident_status() -> Dict:
    return incident_manager.get_status()

@app.get("/metrics")
async def metrics():
    # example metrics
    return {
        "tickets_processed": broker.processed_count,
        "active_workers": 1
    }