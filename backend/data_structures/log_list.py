"""Native Python list wrapper for the real-time log system."""

from backend.models.log_entry import LogEntry


class LogList:
    """Wraps a native Python list to store log entries.

    Provides filtering and searching capabilities for
    real-time log viewing.
    """

    def __init__(self) -> None:
        """Initialize an empty log list."""
        self._logs: list[LogEntry] = []

    # --- Core Operations ---

    def append(self, entry: LogEntry) -> None:
        """Append a new log entry to the list."""
        self._logs.append(entry)

    def get_all(self) -> list[LogEntry]:
        """Return all log entries."""
        return list(self._logs)

    def filter_by_level(self, level: str) -> list[LogEntry]:
        """Return only log entries matching the given level."""
        return [
            entry for entry in self._logs
            if entry.level == level.upper()
        ]

    def search(self, keyword: str) -> list[LogEntry]:
        """Return log entries whose message contains the keyword."""
        keyword_lower = keyword.lower()
        return [
            entry for entry in self._logs
            if keyword_lower in entry.message.lower()
            or keyword_lower in entry.stage.lower()
        ]

    def get_last(self, count: int) -> list[LogEntry]:
        """Return the last N log entries."""
        return self._logs[-count:] if count < len(self._logs) else list(self._logs)

    def clear(self) -> None:
        """Remove all log entries."""
        self._logs.clear()

    # --- State ---

    def size(self) -> int:
        """Return the number of log entries."""
        return len(self._logs)

    def is_empty(self) -> bool:
        """Check if there are no log entries."""
        return len(self._logs) == 0

    # --- Iteration ---

    def __iter__(self):
        return iter(self._logs)

    def __len__(self) -> int:
        return self.size()

    def to_formatted_list(self) -> list[str]:
        """Return formatted strings for all entries."""
        return [entry.formatted() for entry in self._logs]

    def __repr__(self) -> str:
        return f"LogList(size={self.size()})"
