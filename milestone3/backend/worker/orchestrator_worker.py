import asyncio
from typing import Dict, Any

from ml.circuit_breaker import (
    circuit_breaker,
    monitor_model_execution
)

from orchestration.deduplication import Deduplicator
from orchestration.incident_manager import IncidentManager
from orchestration.router import Router
from orchestration.agent_registry import AgentRegistry
from storage.redis_storage import store_ticket

from ml.transformer_model import (
    classify_ticket,
    get_urgency_score
)

from ml.lightweight_model import (
    lightweight_classify,
    lightweight_urgency,
    get_category_vector
)

from utils.locks import lock_manager
from webhook import webhook_client


# --------------------------------------------
# Global Components
# --------------------------------------------

deduplicator = Deduplicator()
incident_manager = IncidentManager()
registry = AgentRegistry()

# --------------------------------------------
# Register Agents
# --------------------------------------------

registry.register_agent(
    "agent_1",
    {"Technical": 1.0, "Billing": 0.2, "Legal": 0.1},
    max_capacity=5
)

registry.register_agent(
    "agent_2",
    {"Technical": 0.3, "Billing": 1.0, "Legal": 0.3},
    max_capacity=4
)

registry.register_agent(
    "agent_3",
    {"Technical": 0.2, "Billing": 0.3, "Legal": 1.0},
    max_capacity=3
)

router = Router(registry)

# Webhook URL (replace with actual mock endpoint)
WEBHOOK_URL = "https://example.com/mock-webhook"

# --------------------------------------------
# Auto Release Agent After Delay
# --------------------------------------------

async def release_agent_after_delay(agent_id: str, delay: int = 5):
    await asyncio.sleep(delay)

    async with lock_manager.get_lock("agent_registry"):
        registry.release_agent(agent_id)

    print(f"🔓 Agent {agent_id} released")

# --------------------------------------------
# Main Ticket Handler
# --------------------------------------------

async def handle_ticket(ticket: Dict[str, Any]):

    ticket_id = ticket.get("ticket_id")
    text = ticket.get("text", "")

    print(f"\n📥 Processing Ticket: {ticket_id}")

    # --------------------------------------------
    # Auto Resolve Old Incidents
    # --------------------------------------------

    async with lock_manager.get_lock("incident"):
        incident_manager.check_and_resolve()

    # --------------------------------------------
    # Model Execution with Circuit Breaker
    # --------------------------------------------

    try:
        if circuit_breaker.allow_request():

            # Automatically measures latency and updates breaker
            with monitor_model_execution():
                category = classify_ticket(text)
                urgency = get_urgency_score(text)

        else:
            raise Exception("Circuit Open")

    except Exception:
        print("⚡ Fallback to lightweight model")
        category = lightweight_classify(text)
        urgency = lightweight_urgency(text)

    # --------------------------------------------
    # Webhook Trigger (Milestone 2 requirement)
    # --------------------------------------------

    if urgency > 0.8:
        await webhook_client.send(
            WEBHOOK_URL,
            {
                "ticket_id": ticket_id,
                "category": category,
                "urgency_score": urgency
            }
        )

    # --------------------------------------------
    # Deduplication
    # --------------------------------------------

    async with lock_manager.get_lock("dedup"):
        dedup_result = deduplicator.process_ticket(text)

    incident_active = False

    if dedup_result["incident"]:
        async with lock_manager.get_lock("incident"):
            incident = incident_manager.handle_incident_trigger()
            incident_active = True
            print(f"🚨 Incident Triggered: {incident.severity}")

    # --------------------------------------------
    # Skill-Based Routing
    # --------------------------------------------

    category_vector = get_category_vector(category)

    async with lock_manager.get_lock("agent_registry"):
        routing = router.route(
            category_vector=category_vector,
            urgency_score=urgency,
            incident_active=incident_active
        )

    if routing is None:
        print("❌ No available agent")
        return

    # --------------------------------------------
    # Final Output
    # --------------------------------------------

    result = {
        "ticket_id": ticket_id,
        "category": category,
        "urgency_score": urgency,
        "is_duplicate": dedup_result["is_duplicate"],
        "duplicate_count": dedup_result["duplicate_count"],
        "incident_active": incident_active,
        "assigned_agent": routing["agent_id"],
        "priority": routing["priority"],
        "circuit_breaker_state": circuit_breaker.get_status()["state"]
    }
    store_ticket(result)
    print("✅ Routed:", result)

    # Auto release agent after simulated processing time
    asyncio.create_task(
        release_agent_after_delay(routing["agent_id"])
    )

    return result