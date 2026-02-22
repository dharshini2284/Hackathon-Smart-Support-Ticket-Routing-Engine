from typing import Dict, Optional

from .agent_registry import AgentRegistry, Agent


# --------------------------------------------
# Router
# --------------------------------------------

class Router:

    def __init__(self, registry: AgentRegistry):
        self.registry = registry

    # --------------------------------------------
    # Route Ticket
    # --------------------------------------------

    def route(
        self,
        category_vector: Dict[str, float],
        urgency_score: float,
        incident_active: bool = False
    ) -> Optional[Dict]:

        best_agent: Agent = self.registry.get_best_agent(
            category_vector
        )

        if not best_agent:
            return None

        # Adjust priority logic
        priority = self._compute_priority(
            urgency_score,
            incident_active
        )

        # Increment load
        self.registry.increment_load(
            best_agent.agent_id
        )

        return {
            "agent_id": best_agent.agent_id,
            "priority": priority,
            "load_ratio": best_agent.load_ratio()
        }

    # --------------------------------------------
    # Priority Calculation
    # --------------------------------------------

    def _compute_priority(
        self,
        urgency_score: float,
        incident_active: bool
    ) -> str:

        if incident_active:
            return "P0"

        if urgency_score >= 0.9:
            return "P0"
        elif urgency_score >= 0.75:
            return "P1"
        elif urgency_score >= 0.5:
            return "P2"
        else:
            return "P3"