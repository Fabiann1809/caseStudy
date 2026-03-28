"""Service that manages the job queue."""

from backend.data_structures.job_queue import JobQueue
from backend.models.job import Job
from backend.services.agent_manager import AgentManager


class JobQueueService:
    """Manages job submission and processing through the FIFO queue.

    Jobs are enqueued when developers push code and dequeued when
    an execution agent becomes available.
    """

    def __init__(self, job_queue: JobQueue) -> None:
        """Initialize with a job queue instance."""
        self._queue: JobQueue = job_queue
        self._completed_jobs: list[Job] = []

    # --- Submit ---

    def submit_job(
        self, name: str, developer: str, branch: str
    ) -> Job:
        """Create a new job and add it to the queue."""
        job = Job(name=name, developer=developer, branch=branch)
        self._queue.enqueue(job)
        return job

    # --- Process ---

    def process_next(self, agent_manager: AgentManager) -> dict:
        """Attempt to assign the next job in the queue to an agent.

        Returns a result dict with the outcome.
        """
        if self._queue.is_empty():
            return {
                "success": False,
                "reason": "La cola de trabajos está vacía.",
            }

        if not agent_manager.has_available():
            return {
                "success": False,
                "reason": "No hay agentes disponibles. Todos los servidores están ocupados.",
            }

        job = self._queue.dequeue()
        agent_index = agent_manager.assign_job_to_agent(job)

        agent = agent_manager.get_agent(agent_index)
        return {
            "success": True,
            "job": job,
            "agent_index": agent_index,
            "agent_name": agent.name,
            "message": (
                f"Trabajo '{job.name}' asignado al agente "
                f"'{agent.name}' ({agent.os_type})."
            ),
        }

    def complete_job(
        self, agent_manager: AgentManager, agent_index: int, success: bool = True
    ) -> dict:
        """Complete the job running on the given agent."""
        agent = agent_manager.get_agent(agent_index)
        job = agent.current_job
        if job is None:
            return {
                "success": False,
                "reason": f"El agente '{agent.name}' no tiene un trabajo asignado.",
            }

        job.complete(success=success)
        agent_manager.release_agent(agent_index)
        self._completed_jobs.append(job)
        status_text = "exitosamente" if success else "con errores"
        return {
            "success": True,
            "job": job,
            "message": (
                f"Trabajo '{job.name}' finalizado {status_text} "
                f"en '{agent.name}'."
            ),
        }

    # --- Query ---

    def get_pending_jobs(self) -> list[dict]:
        """Return serialized list of pending jobs."""
        return self._queue.to_list()

    def get_completed_jobs(self) -> list[dict]:
        """Return serialized list of completed jobs."""
        return [job.to_dict() for job in self._completed_jobs]

    def get_queue_size(self) -> int:
        """Return number of jobs waiting in the queue."""
        return self._queue.size()

    @property
    def queue(self) -> JobQueue:
        return self._queue

    def __repr__(self) -> str:
        return (
            f"JobQueueService(pending={self._queue.size()}, "
            f"completed={len(self._completed_jobs)})"
        )
