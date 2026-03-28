"""Job model representing a build/compilation task."""

import uuid
from datetime import datetime


class Job:
    """Represents a CI/CD job submitted by a developer.

    A job goes through the lifecycle: queued -> running -> success/failed.
    """

    VALID_STATUSES = ("queued", "running", "success", "failed")

    def __init__(self, name: str, developer: str, branch: str) -> None:
        self._id: str = str(uuid.uuid4())[:8]
        self._name: str = name
        self._developer: str = developer
        self._branch: str = branch
        self._status: str = "queued"
        self._created_at: datetime = datetime.now()
        self._started_at: datetime | None = None
        self._finished_at: datetime | None = None

    # --- Properties ---

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def developer(self) -> str:
        return self._developer

    @property
    def branch(self) -> str:
        return self._branch

    @property
    def status(self) -> str:
        return self._status

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def started_at(self) -> datetime | None:
        return self._started_at

    @property
    def finished_at(self) -> datetime | None:
        return self._finished_at

    # --- Methods ---

    def start(self) -> None:
        """Mark the job as running."""
        self._status = "running"
        self._started_at = datetime.now()

    def complete(self, success: bool = True) -> None:
        """Mark the job as finished (success or failed)."""
        self._status = "success" if success else "failed"
        self._finished_at = datetime.now()

    def to_dict(self) -> dict:
        """Serialize job state to a dictionary."""
        return {
            "id": self._id,
            "name": self._name,
            "developer": self._developer,
            "branch": self._branch,
            "status": self._status,
            "created_at": self._created_at.strftime("%H:%M:%S"),
            "started_at": (
                self._started_at.strftime("%H:%M:%S")
                if self._started_at else None
            ),
            "finished_at": (
                self._finished_at.strftime("%H:%M:%S")
                if self._finished_at else None
            ),
        }

    def __repr__(self) -> str:
        return (
            f"Job(id='{self._id}', name='{self._name}', "
            f"status='{self._status}')"
        )
