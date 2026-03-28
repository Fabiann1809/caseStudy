"""Service that manages the fixed array of execution agents."""

from typing import Optional
from backend.data_structures.agent_array import AgentArray
from backend.models.agent import Agent
from backend.models.job import Job


class AgentManager:
    """Manages the agent array — finding, assigning, and releasing agents.

    Provides a high-level interface over the AgentArray data structure.
    """

    def __init__(self) -> None:
        """Initialize the manager with the predefined agents."""
        self._agent_array: AgentArray = AgentArray()

    # --- Query ---

    def get_agents(self) -> list[Agent]:
        """Return all agents in the array."""
        return list(self._agent_array)

    def get_agent(self, index: int) -> Agent:
        """Return the agent at the given index."""
        return self._agent_array.get(index)

    def get_available_agents(self) -> list[tuple[int, Agent]]:
        """Return (index, agent) pairs for idle agents."""
        return self._agent_array.get_available()

    def get_busy_agents(self) -> list[tuple[int, Agent]]:
        """Return (index, agent) pairs for busy agents."""
        return self._agent_array.get_busy()

    def has_available(self) -> bool:
        """Check if at least one agent is available."""
        return len(self._agent_array.get_available()) > 0

    # --- Actions ---

    def assign_job_to_agent(self, job: Job) -> Optional[int]:
        """Assign a job to the first available agent.

        Returns the index of the agent, or None if no agent is free.
        """
        available = self._agent_array.get_available()
        if not available:
            return None
        index, agent = available[0]
        self._agent_array.assign_job(index, job)
        job.start()
        return index

    def release_agent(self, index: int) -> None:
        """Release the agent at the given index."""
        self._agent_array.release(index)

    # --- Summary ---

    def get_status_summary(self) -> dict:
        """Return a summary of all agents and their statuses."""
        return {
            "total": len(self._agent_array),
            "available": len(self._agent_array.get_available()),
            "busy": len(self._agent_array.get_busy()),
            "agents": [a.to_dict() for a in self._agent_array],
        }

    def __repr__(self) -> str:
        return f"AgentManager({self._agent_array})"
