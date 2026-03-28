"""Pipeline stage model representing a single step in the CI/CD pipeline."""

import random


class PipelineStage:
    """Represents one stage of the pipeline execution.

    Each stage has a name, a status, and a simulated duration.
    """

    VALID_STATUSES = ("pending", "running", "success", "failed", "skipped")

    def __init__(self, name: str, duration_seconds: float = 0.0) -> None:
        self._name: str = name
        self._status: str = "pending"
        self._duration_seconds: float = duration_seconds
        self._output: str = ""

    # --- Properties ---

    @property
    def name(self) -> str:
        return self._name

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        if value not in self.VALID_STATUSES:
            raise ValueError(
                f"Invalid status '{value}'. "
                f"Must be one of {self.VALID_STATUSES}"
            )
        self._status = value

    @property
    def duration_seconds(self) -> float:
        return self._duration_seconds

    @property
    def output(self) -> str:
        return self._output

    @output.setter
    def output(self, value: str) -> None:
        self._output = value

    # --- Methods ---

    def execute(self, fail_probability: float = 0.15) -> bool:
        """Simulate executing this stage.

        Returns True if the stage passed, False if it failed.
        """
        self._status = "running"
        self._duration_seconds = round(random.uniform(0.5, 3.0), 2)

        passed = random.random() > fail_probability
        if passed:
            self._status = "success"
            self._output = f"Stage '{self._name}' completed successfully."
        else:
            self._status = "failed"
            self._output = (
                f"Stage '{self._name}' failed — "
                f"error code {random.randint(1, 127)}."
            )
        return passed

    def reset(self) -> None:
        """Reset the stage to pending state."""
        self._status = "pending"
        self._duration_seconds = 0.0
        self._output = ""

    def to_dict(self) -> dict:
        """Serialize stage state to a dictionary."""
        return {
            "name": self._name,
            "status": self._status,
            "duration": self._duration_seconds,
            "output": self._output,
        }

    def __repr__(self) -> str:
        return (
            f"PipelineStage(name='{self._name}', "
            f"status='{self._status}')"
        )
