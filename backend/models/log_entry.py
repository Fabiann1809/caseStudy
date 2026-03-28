"""Log entry model for the real-time log system."""

from datetime import datetime


class LogEntry:
    """Represents a single log entry in the CI/CD system.

    Entries are appended to a native Python list for real-time viewing.
    """

    VALID_LEVELS = ("INFO", "WARN", "ERROR", "DEBUG", "SUCCESS")

    def __init__(
        self,
        level: str,
        stage: str,
        message: str,
    ) -> None:
        if level not in self.VALID_LEVELS:
            raise ValueError(
                f"Invalid log level '{level}'. "
                f"Must be one of {self.VALID_LEVELS}"
            )
        self._timestamp: datetime = datetime.now()
        self._level: str = level
        self._stage: str = stage
        self._message: str = message

    # --- Properties ---

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    def level(self) -> str:
        return self._level

    @property
    def stage(self) -> str:
        return self._stage

    @property
    def message(self) -> str:
        return self._message

    # --- Methods ---

    def formatted(self) -> str:
        """Return a formatted log line for console display."""
        time_str = self._timestamp.strftime("%H:%M:%S")
        return f"[{time_str}] [{self._level:<7}] [{self._stage}] {self._message}"

    def to_dict(self) -> dict:
        """Serialize log entry to a dictionary."""
        return {
            "timestamp": self._timestamp.strftime("%H:%M:%S"),
            "level": self._level,
            "stage": self._stage,
            "message": self._message,
        }

    def __repr__(self) -> str:
        return (
            f"LogEntry(level='{self._level}', "
            f"stage='{self._stage}', "
            f"message='{self._message[:30]}...')"
        )
