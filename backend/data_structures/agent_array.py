"""Fixed-size array of execution agents (virtual servers)."""

from typing import Optional
from backend.models.agent import Agent


class AgentArray:
    """Wraps a fixed-size Python list representing the available
    execution agents in the CI/CD system.

    The array has exactly 4 slots, one per predefined virtual server.
    """

    PREDEFINED_AGENTS = [
        ("ubuntu-server", "Ubuntu"),
        ("windows-server", "Windows"),
        ("macos-server", "macOS"),
        ("alpine-server", "Alpine"),
    ]

    def __init__(self) -> None:
        """Initialize the fixed array with the 4 predefined agents."""
        self._agents: list[Agent] = [
            Agent(name=name, os_type=os_type)
            for name, os_type in self.PREDEFINED_AGENTS
        ]

    # --- Access ---

    def get(self, index: int) -> Agent:
        """Return the agent at the given index."""
        if not 0 <= index < len(self._agents):
            raise IndexError(
                f"Index {index} out of range (0-{len(self._agents) - 1})."
            )
        return self._agents[index]

    def get_available(self) -> list[tuple[int, Agent]]:
        """Return a list of (index, agent) for agents that are idle."""
        return [
            (i, agent) for i, agent in enumerate(self._agents)
            if agent.is_available()
        ]

    def get_busy(self) -> list[tuple[int, Agent]]:
        """Return a list of (index, agent) for agents that are busy."""
        return [
            (i, agent) for i, agent in enumerate(self._agents)
            if not agent.is_available()
        ]

    def assign_job(self, index: int, job: object) -> None:
        """Assign a job to the agent at the given index."""
        agent = self.get(index)
        agent.assign_job(job)

    def release(self, index: int) -> None:
        """Release the agent at the given index."""
        agent = self.get(index)
        agent.release()

    # --- Iteration ---

    def __len__(self) -> int:
        return len(self._agents)

    def __iter__(self):
        return iter(self._agents)

    def __getitem__(self, index: int) -> Agent:
        return self.get(index)

    def __repr__(self) -> str:
        available = len(self.get_available())
        total = len(self._agents)
        return f"AgentArray(available={available}/{total})"
