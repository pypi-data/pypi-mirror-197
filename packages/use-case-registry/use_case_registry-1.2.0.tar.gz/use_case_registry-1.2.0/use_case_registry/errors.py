"""Custom defined errors."""

from typing import Any

from use_case_registry import UseCaseRegistry


class CommandInputValidationError(Exception):
    """Raised when command input values does pass validation check."""


class UseCaseExecutionError(Exception):
    """Raised when there's an error executing a workflow."""

    def __init__(self, error: Exception) -> None:
        """Construct class."""
        super().__init__(f"Error executing a use case {error}")


class CommitTransactionsError(Exception):
    """Raised when there's an error committing a set of transactions."""

    def __init__(self, transactions: UseCaseRegistry[Any]) -> None:
        """Construct class."""
        super().__init__(f"Error commiting transactions {transactions}")
