import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

from ticket_queue.redis_client import RedisBroker
from worker.orchestrator_worker import handle_ticket
from worker.orchestrator_worker import incident_manager
from storage.redis_storage import get_all_tickets
from worker.orchestrator_worker import registry
from ml.circuit_breaker import circuit_breaker
from worker.orchestrator_worker import deduplicator
from orchestration.deduplication import get_flood_metrics
from faker import Faker
import random

# --------------------------------------------
# FastAPI App
# --------------------------------------------

app = FastAPI(title="AI Ticket Orchestrator")
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",  # your frontend URL
    "http://127.0.0.1:5173",
    "https://smart-support-ticket-routing-engine-frontend-l9nnx9v4r.vercel.app"
    # you can add more origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, etc.
    allow_headers=["*"],  # Authorization, Content-Type, etc.
)
# Broker + Incident Manager
# --------------------------------------------

broker = RedisBroker()
# incident_manager is imported from worker.orchestrator_worker

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
    agents_data = []

    for agent in registry.agents.values():
        load_ratio = agent.current_load / agent.max_capacity

        if load_ratio < 0.5:
            status = "healthy"
        elif load_ratio < 1:
            status = "degraded"
        else:
            status = "down"

        agents_data.append({
            "name": agent.agent_id,
            "status": status,
            "latency": round(load_ratio * 500)  # simulated metric
        })

    return {
        "tickets_processed": broker.processed_count,
        "active_workers": 1,
        "agents": agents_data,
        "circuit_breaker": circuit_breaker.get_status(),
        "flash_flood": get_flood_metrics(deduplicator),
    }

@app.get("/tickets")
async def get_tickets():
    return get_all_tickets()

from faker import Faker
import random

fake = Faker()

@app.post("/simulate")
async def simulate_tickets(
    num_tickets: int = 10,
    duplicate_ratio: float = 0.1
):
    for i in range(num_tickets):

        if random.random() < duplicate_ratio:
            ticket = {
                "ticket_id": f"SIM-DUP-{i}",
                "text": "Server outage in region X ASAP"
            }
        else:
            ticket = {
                "ticket_id": f"SIM-{i}",
                "text": fake.text(max_nb_chars=100)
            }
        await asyncio.sleep(0.05)
        await broker.publish(ticket)

    return {
        "message": f"{num_tickets} tickets submitted for simulation"
    }