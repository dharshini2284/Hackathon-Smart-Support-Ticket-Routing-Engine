import time
from typing import Dict, List, Optional


# --------------------------------------------
# Configuration
# --------------------------------------------

INCIDENT_TIMEOUT = 300  # auto-resolve after 5 mins inactivity


# --------------------------------------------
# Incident Model
# --------------------------------------------

class Incident:

    def __init__(self, incident_id: str):
        self.incident_id = incident_id
        self.created_at = time.time()
        self.last_updated = time.time()
        self.ticket_count = 0
        self.severity = "LOW"
        self.status = "ACTIVE"

    def update(self):
        self.ticket_count += 1
        self.last_updated = time.time()
        self._update_severity()

    def _update_severity(self):
        if self.ticket_count >= 20:
            self.severity = "CRITICAL"
        elif self.ticket_count >= 10:
            self.severity = "HIGH"
        elif self.ticket_count >= 5:
            self.severity = "MEDIUM"
        else:
            self.severity = "LOW"

    def is_expired(self) -> bool:
        return (
            time.time() - self.last_updated
        ) > INCIDENT_TIMEOUT

    def resolve(self):
        self.status = "RESOLVED"


# --------------------------------------------
# Incident Manager
# --------------------------------------------

class IncidentManager:

    def __init__(self):
        self.active_incident: Optional[Incident] = None
        self.incident_history: List[Incident] = []

    # --------------------------------------------
    # Handle Incident Trigger
    # --------------------------------------------

    def handle_incident_trigger(self) -> Incident:

        if self.active_incident is None:
            self.active_incident = Incident(
                incident_id=f"INC-{int(time.time())}"
            )

        self.active_incident.update()

        return self.active_incident

    # --------------------------------------------
    # Periodic Cleanup
    # --------------------------------------------

    def check_and_resolve(self):

        if self.active_incident and \
           self.active_incident.is_expired():

            self.active_incident.resolve()
            self.incident_history.append(
                self.active_incident
            )

            self.active_incident = None

    # --------------------------------------------
    # Get Current Status
    # --------------------------------------------

    def get_status(self) -> Dict:

        if self.active_incident:
            return {
                "incident_id": self.active_incident.incident_id,
                "severity": self.active_incident.severity,
                "ticket_count": self.active_incident.ticket_count,
                "status": self.active_incident.status
            }

        return {
            "status": "NO_ACTIVE_INCIDENT"
        }