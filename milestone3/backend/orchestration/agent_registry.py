from typing import Dict, List
import math

# --------------------------------------------
# Agent Model
# --------------------------------------------

class Agent:
    def __init__(
        self,
        agent_id: str,
        skills: Dict[str, float],
        max_capacity: int = 5
    ):
        self.agent_id = agent_id
        self.skills = skills
        self.current_load = 0
        self.max_capacity = max_capacity

    def load_ratio(self) -> float:
        if self.max_capacity == 0:
            return 1.0
        return self.current_load / self.max_capacity


# --------------------------------------------
# Agent Registry
# --------------------------------------------

class AgentRegistry:

    def __init__(self):
        self.agents: Dict[str, Agent] = {}

    # -----------------------------
    # Register Agent
    # -----------------------------

    def register_agent(
        self,
        agent_id: str,
        skills: Dict[str, float],
        max_capacity: int = 5
    ):
        self.agents[agent_id] = Agent(
            agent_id,
            skills,
            max_capacity
        )

    # -----------------------------
    # Get Best Agent
    # -----------------------------

    def get_best_agent(
        self,
        category_vector: Dict[str, float]
    ) -> Agent:

        best_score = -math.inf
        best_agent = None

        for agent in self.agents.values():

            # Skip overloaded agents
            if agent.current_load >= agent.max_capacity:
                continue

            skill_score = self._compute_skill_match(
                agent.skills,
                category_vector
            )

            load_score = 1 - agent.load_ratio()

            final_score = (skill_score * 0.7) + (load_score * 0.3)

            if final_score > best_score:
                best_score = final_score
                best_agent = agent

        return best_agent

    # -----------------------------
    # Update Load
    # -----------------------------

    def increment_load(self, agent_id: str):
        if agent_id in self.agents:
            self.agents[agent_id].current_load += 1

    def decrement_load(self, agent_id: str):
        if agent_id in self.agents:
            self.agents[agent_id].current_load = max(
                0,
                self.agents[agent_id].current_load - 1
            )

    # -----------------------------
    # Skill Matching (Dot Product)
    # -----------------------------

    def _compute_skill_match(
        self,
        agent_skills: Dict[str, float],
        category_vector: Dict[str, float]
    ) -> float:

        score = 0.0

        for key in category_vector:
            score += (
                agent_skills.get(key, 0.0)
                * category_vector.get(key, 0.0)
            )

        return score