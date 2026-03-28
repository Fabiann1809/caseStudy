"""Singly linked list for pipeline stage definitions."""

from typing import Optional
from backend.models.pipeline_stage import PipelineStage


class StageNode:
    """A node in the singly linked list of pipeline stages.

    Each node holds a PipelineStage and a reference to the next node.
    A stage can only invoke the next stage once it finishes successfully.
    """

    def __init__(self, stage: PipelineStage) -> None:
        self._stage: PipelineStage = stage
        self._next: Optional["StageNode"] = None

    @property
    def stage(self) -> PipelineStage:
        return self._stage

    @property
    def next(self) -> Optional["StageNode"]:
        return self._next

    @next.setter
    def next(self, node: Optional["StageNode"]) -> None:
        self._next = node

    def __repr__(self) -> str:
        next_name = self._next.stage.name if self._next else "None"
        return (
            f"StageNode('{self._stage.name}' -> '{next_name}')"
        )


class StageLinkedList:
    """Singly linked list of pipeline stages.

    Stages are traversed sequentially: each stage can only
    invoke the next one after it finishes successfully.
    """

    # Default pipeline stages
    DEFAULT_STAGES = [
        "Checkout",
        "Instalar Dependencias",
        "Linter",
        "Pruebas Unitarias",
        "Despliegue",
    ]

    def __init__(self) -> None:
        """Initialize an empty linked list."""
        self._head: Optional[StageNode] = None
        self._size: int = 0

    # --- Core Operations ---

    def append(self, stage: PipelineStage) -> None:
        """Append a stage node at the end of the list."""
        new_node = StageNode(stage)
        if self._head is None:
            self._head = new_node
        else:
            current = self._head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self._size += 1

    def get_head(self) -> Optional[StageNode]:
        """Return the first node in the list."""
        return self._head

    def get_stage_at(self, index: int) -> Optional[PipelineStage]:
        """Return the stage at the given position."""
        current = self._head
        count = 0
        while current is not None:
            if count == index:
                return current.stage
            current = current.next
            count += 1
        return None

    def reset_all(self) -> None:
        """Reset all stages to pending status."""
        current = self._head
        while current is not None:
            current.stage.reset()
            current = current.next

    # --- Class Method to build default pipeline ---

    @classmethod
    def build_default(cls) -> "StageLinkedList":
        """Create a linked list with the default pipeline stages."""
        linked_list = cls()
        for name in cls.DEFAULT_STAGES:
            stage = PipelineStage(name=name)
            linked_list.append(stage)
        return linked_list

    # --- Iteration ---

    def __iter__(self):
        current = self._head
        while current is not None:
            yield current.stage
            current = current.next

    def __len__(self) -> int:
        return self._size

    def to_list(self) -> list[dict]:
        """Return a serialized list of all stages."""
        return [stage.to_dict() for stage in self]

    def __repr__(self) -> str:
        names = [stage.name for stage in self]
        return f"StageLinkedList({' -> '.join(names)})"
