"""Service for real-time log management."""

from backend.data_structures.log_list import LogList
from backend.models.log_entry import LogEntry


class LogService:
    """Manages the log list for real-time log viewing.

    Provides methods to add, filter, and search log entries.
    """

    def __init__(self, log_list: LogList) -> None:
        """Initialize with a log list instance."""
        self._log_list: LogList = log_list

    # --- Add ---

    def add_log(
        self,
        level: str,
        stage: str,
        message: str,
    ) -> LogEntry:
        """Create and append a new log entry."""
        entry = LogEntry(level=level, stage=stage, message=message)
        self._log_list.append(entry)
        return entry

    def info(self, stage: str, message: str) -> LogEntry:
        """Shortcut to add an INFO-level log."""
        return self.add_log("INFO", stage, message)

    def warn(self, stage: str, message: str) -> LogEntry:
        """Shortcut to add a WARN-level log."""
        return self.add_log("WARN", stage, message)

    def error(self, stage: str, message: str) -> LogEntry:
        """Shortcut to add an ERROR-level log."""
        return self.add_log("ERROR", stage, message)

    def success(self, stage: str, message: str) -> LogEntry:
        """Shortcut to add a SUCCESS-level log."""
        return self.add_log("SUCCESS", stage, message)

    def debug(self, stage: str, message: str) -> LogEntry:
        """Shortcut to add a DEBUG-level log."""
        return self.add_log("DEBUG", stage, message)

    # --- Query ---

    def get_logs(self) -> list[LogEntry]:
        """Return all log entries."""
        return self._log_list.get_all()

    def filter_logs(self, level: str) -> list[LogEntry]:
        """Return entries matching the given level."""
        return self._log_list.filter_by_level(level)

    def search_logs(self, keyword: str) -> list[LogEntry]:
        """Return entries matching the keyword."""
        return self._log_list.search(keyword)

    def get_formatted_logs(self) -> list[str]:
        """Return all entries as formatted strings."""
        return self._log_list.to_formatted_list()

    def get_last_logs(self, count: int = 50) -> list[LogEntry]:
        """Return the last N log entries."""
        return self._log_list.get_last(count)

    def clear_logs(self) -> None:
        """Clear all log entries."""
        self._log_list.clear()

    def get_log_count(self) -> int:
        """Return the total number of log entries."""
        return self._log_list.size()

    @property
    def log_list(self) -> LogList:
        return self._log_list

    def __repr__(self) -> str:
        return f"LogService(entries={self._log_list.size()})"
