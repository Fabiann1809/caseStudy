"""Agent model representing a virtual execution server."""

from datetime import datetime
from typing import Optional


class Agent:
    """Represents a virtual server (execution agent) in the CI/CD system.

    Each agent can run one job at a time and has a specific operating system.
    """

    VALID_OS_TYPES = ("Ubuntu", "Windows", "macOS", "Alpine")

    def __init__(self, name: str, os_type: str) -> None:
        if os_type not in self.VALID_OS_TYPES:
            raise ValueError(
                f"Invalid OS type '{os_type}'. "
                f"Must be one of {self.VALID_OS_TYPES}"
            )
        self._name: str = name
        self._os_type: str = os_type
        self._status: str = "idle"  # idle | busy
        self._current_job: Optional[object] = None
        self._jobs_completed: int = 0
        self._last_active: Optional[datetime] = None

    # --- Properties ---

    @property
    def name(self) -> str:
        return self._name

    @property
    def os_type(self) -> str:
        return self._os_type

    @property
    def status(self) -> str:
        return self._status

    @property
    def current_job(self) -> Optional[object]:
        return self._current_job

    @property
    def jobs_completed(self) -> int:
        return self._jobs_completed

    @property
    def last_active(self) -> Optional[datetime]:
        return self._last_active

    # --- Methods ---

    def is_available(self) -> bool:
        """Check if the agent is available to take a new job."""
        return self._status == "idle"

    def assign_job(self, job: object) -> None:
        """Assign a job to this agent, marking it as busy."""
        if not self.is_available():
            raise RuntimeError(
                f"Agent '{self._name}' is already busy."
            )
        self._current_job = job
        self._status = "busy"
        self._last_active = datetime.now()

    def release(self) -> None:
        """Release the agent after a job finishes."""
        self._current_job = None
        self._status = "idle"
        self._jobs_completed += 1

    def to_dict(self) -> dict:
        """Serialize agent state to a dictionary."""
        return {
            "name": self._name,
            "os_type": self._os_type,
            "status": self._status,
            "current_job": (
                self._current_job.name if self._current_job else None
            ),
            "jobs_completed": self._jobs_completed,
            "last_active": (
                self._last_active.isoformat() if self._last_active else None
            ),
        }

    def __repr__(self) -> str:
        return (
            f"Agent(name='{self._name}', os='{self._os_type}', "
            f"status='{self._status}')"
        )
