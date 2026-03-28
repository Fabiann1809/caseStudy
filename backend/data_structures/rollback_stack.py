"""LIFO stack for deployment rollback management."""

from typing import Optional
from backend.models.deployment import Deployment


class RollbackStack:
    """Last-In-First-Out stack of production deployments.

    Each successful deployment is pushed onto this stack. When the
    current version fails, the 'Emergency Rollback' pops the top
    and restores the previous deployment.
    """

    def __init__(self) -> None:
        """Initialize an empty deployment stack."""
        self._stack: list[Deployment] = []

    # --- Core Stack Operations ---

    def push(self, deployment: Deployment) -> None:
        """Push a new deployment onto the top of the stack."""
        self._stack.append(deployment)

    def pop(self) -> Deployment:
        """Remove and return the deployment on top of the stack.

        Raises IndexError if the stack is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack.")
        return self._stack.pop()

    def peek(self) -> Optional[Deployment]:
        """Return the deployment on top without removing it."""
        if self.is_empty():
            return None
        return self._stack[-1]

    # --- State ---

    def is_empty(self) -> bool:
        """Check whether the stack has no deployments."""
        return len(self._stack) == 0

    def size(self) -> int:
        """Return the number of deployments on the stack."""
        return len(self._stack)

    # --- Iteration (top to bottom) ---

    def __iter__(self):
        return iter(reversed(self._stack))

    def __len__(self) -> int:
        return self.size()

    def to_list(self) -> list[dict]:
        """Return a serialized list of deployments (top first)."""
        return [d.to_dict() for d in reversed(self._stack)]

    def __repr__(self) -> str:
        top = self.peek()
        top_str = top.version if top else "empty"
        return f"RollbackStack(size={self.size()}, top='{top_str}')"
