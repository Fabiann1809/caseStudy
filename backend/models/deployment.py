"""Deployment model representing a version pushed to production."""

import uuid
from datetime import datetime


class Deployment:
    """Represents a production deployment that can be rolled back.

    Each deployment records its version, commit hash, and timestamp.
    """

    def __init__(
        self,
        version: str,
        commit_hash: str | None = None,
        status: str = "active",
    ) -> None:
        self._id: str = str(uuid.uuid4())[:8]
        self._version: str = version
        self._commit_hash: str = commit_hash or str(uuid.uuid4())[:7]
        self._status: str = status  # active | rolled_back
        self._deployed_at: datetime = datetime.now()

    # --- Properties ---

    @property
    def id(self) -> str:
        return self._id

    @property
    def version(self) -> str:
        return self._version

    @property
    def commit_hash(self) -> str:
        return self._commit_hash

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        self._status = value

    @property
    def deployed_at(self) -> datetime:
        return self._deployed_at

    # --- Methods ---

    def to_dict(self) -> dict:
        """Serialize deployment state to a dictionary."""
        return {
            "id": self._id,
            "version": self._version,
            "commit_hash": self._commit_hash,
            "status": self._status,
            "deployed_at": self._deployed_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def __repr__(self) -> str:
        return (
            f"Deployment(version='{self._version}', "
            f"commit='{self._commit_hash}', "
            f"status='{self._status}')"
        )
