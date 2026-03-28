"""FIFO queue for CI/CD jobs awaiting execution."""

from collections import deque
from typing import Optional
from backend.models.job import Job


class JobQueue:
    """First-In-First-Out queue for build/compilation jobs.

    When multiple developers push simultaneously, their jobs enter
    this queue and wait until an execution agent becomes available.
    """

    def __init__(self) -> None:
        """Initialize an empty job queue."""
        self._queue: deque[Job] = deque()

    # --- Core Queue Operations ---

    def enqueue(self, job: Job) -> None:
        """Add a job to the back of the queue."""
        self._queue.append(job)

    def dequeue(self) -> Job:
        """Remove and return the job at the front of the queue.

        Raises IndexError if the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue.")
        return self._queue.popleft()

    def peek(self) -> Optional[Job]:
        """Return the job at the front without removing it."""
        if self.is_empty():
            return None
        return self._queue[0]

    # --- State ---

    def is_empty(self) -> bool:
        """Check whether the queue has no jobs."""
        return len(self._queue) == 0

    def size(self) -> int:
        """Return the number of jobs currently in the queue."""
        return len(self._queue)

    # --- Iteration ---

    def __iter__(self):
        return iter(self._queue)

    def __len__(self) -> int:
        return self.size()

    def to_list(self) -> list[dict]:
        """Return a serialized list of all jobs in the queue."""
        return [job.to_dict() for job in self._queue]

    def __repr__(self) -> str:
        return f"JobQueue(size={self.size()})"
