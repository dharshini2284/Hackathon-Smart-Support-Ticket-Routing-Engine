import time
import redis
import json
from contextlib import contextmanager

# Redis connection
redis_client = redis.Redis(host="localhost", port=6379, db=0)

# Circuit breaker Redis key
CB_KEY = "circuit_breaker_state"

# Configurable thresholds
LATENCY_THRESHOLD_MS = 500
FAILURE_THRESHOLD = 3
RECOVERY_TIMEOUT = 10  # seconds before attempting HALF-OPEN


class CircuitBreaker:
    """
    Production-grade Circuit Breaker with:
    - CLOSED
    - OPEN
    - HALF-OPEN
    """

    def __init__(self):
        self._initialize_state()

    def _initialize_state(self):
        if not redis_client.exists(CB_KEY):
            state = {
                "state": "CLOSED",
                "failure_count": 0,
                "last_failure_time": None,
                "last_latency_ms": 0
            }
            redis_client.set(CB_KEY, json.dumps(state))

    def _get_state(self):
        data = redis_client.get(CB_KEY)
        return json.loads(data)

    def _set_state(self, state_dict):
        redis_client.set(CB_KEY, json.dumps(state_dict))

    def record_success(self, latency_ms):
        state = self._get_state()

        state["failure_count"] = 0
        state["last_latency_ms"] = latency_ms

        if state["state"] == "HALF-OPEN":
            # Successful recovery → close breaker
            state["state"] = "CLOSED"

        self._set_state(state)

    def record_failure(self, latency_ms):
        state = self._get_state()

        state["failure_count"] += 1
        state["last_failure_time"] = time.time()
        state["last_latency_ms"] = latency_ms

        if state["failure_count"] >= FAILURE_THRESHOLD:
            state["state"] = "OPEN"

        self._set_state(state)

    def allow_request(self):
        """
        Determines whether Transformer model should be used
        """
        state = self._get_state()

        if state["state"] == "CLOSED":
            return True

        if state["state"] == "OPEN":
            # Check if recovery timeout passed
            if state["last_failure_time"] is None:
                return False

            if time.time() - state["last_failure_time"] > RECOVERY_TIMEOUT:
                state["state"] = "HALF-OPEN"
                self._set_state(state)
                return True

            return False

        if state["state"] == "HALF-OPEN":
            return True

        return True

    def get_status(self):
        return self._get_state()


# Singleton instance
circuit_breaker = CircuitBreaker()


@contextmanager
def monitor_model_execution():
    """
    Wrap Transformer model execution inside this context
    Automatically handles:
    - Latency measurement
    - Failure detection
    - State transitions
    """
    start = time.time()
    try:
        yield
        latency_ms = (time.time() - start) * 1000

        if latency_ms > LATENCY_THRESHOLD_MS:
            circuit_breaker.record_failure(latency_ms)
        else:
            circuit_breaker.record_success(latency_ms)

    except Exception:
        latency_ms = (time.time() - start) * 1000
        circuit_breaker.record_failure(latency_ms)
        raise