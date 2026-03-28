"""Service that manages the deployment rollback stack."""

from typing import Optional
from backend.data_structures.rollback_stack import RollbackStack
from backend.models.deployment import Deployment


class RollbackService:
    """Manages the deployment stack for rollback operations.

    Each successful deploy pushes a version onto the stack.
    Emergency rollback pops the current version and restores
    the previous one.
    """

    def __init__(self, rollback_stack: RollbackStack) -> None:
        """Initialize with a rollback stack instance."""
        self._stack: RollbackStack = rollback_stack
        self._rolled_back: list[Deployment] = []

    # --- Deploy ---

    def push_deployment(
        self,
        version: str,
        commit_hash: str | None = None,
    ) -> Deployment:
        """Push a new deployment version onto the stack."""
        deployment = Deployment(
            version=version,
            commit_hash=commit_hash,
            status="active",
        )
        # Mark previous top as superseded
        previous = self._stack.peek()
        if previous:
            previous.status = "superseded"

        self._stack.push(deployment)
        return deployment

    # --- Rollback ---

    def emergency_rollback(self) -> dict:
        """Pop the current deployment and restore the previous one.

        Returns a result dict with the outcome.
        """
        if self._stack.is_empty():
            return {
                "success": False,
                "reason": "No hay despliegues en la pila para revertir.",
            }

        if self._stack.size() == 1:
            return {
                "success": False,
                "reason": "Solo queda un despliegue. No se puede revertir más.",
            }

        rolled_back = self._stack.pop()
        rolled_back.status = "rolled_back"
        self._rolled_back.append(rolled_back)

        restored = self._stack.peek()
        if restored:
            restored.status = "active"

        return {
            "success": True,
            "rolled_back_version": rolled_back.version,
            "restored_version": restored.version if restored else None,
            "message": (
                f"¡Rollback exitoso! Versión '{rolled_back.version}' "
                f"revertida. Restaurada versión '{restored.version}'."
            ),
        }

    # --- Query ---

    def get_current_version(self) -> Optional[Deployment]:
        """Return the current (top) deployment."""
        return self._stack.peek()

    def get_history(self) -> list[dict]:
        """Return the deployment history (top first)."""
        return self._stack.to_list()

    def get_rolled_back_history(self) -> list[dict]:
        """Return deployments that were rolled back."""
        return [d.to_dict() for d in self._rolled_back]

    def get_stack_size(self) -> int:
        """Return the number of deployments on the stack."""
        return self._stack.size()

    @property
    def stack(self) -> RollbackStack:
        return self._stack

    def __repr__(self) -> str:
        current = self.get_current_version()
        ver = current.version if current else "none"
        return (
            f"RollbackService(current='{ver}', "
            f"stack_size={self._stack.size()})"
        )
