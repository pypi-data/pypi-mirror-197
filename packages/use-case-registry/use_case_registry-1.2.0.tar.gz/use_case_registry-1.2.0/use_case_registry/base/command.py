"""Interface for concrete commands."""
import abc
from typing import Any

from result import Result

from use_case_registry import UseCaseRegistry
from use_case_registry.errors import CommandInputValidationError, UseCaseExecutionError


class ICommand(abc.ABC):
    """Command interface."""

    @abc.abstractmethod
    def validate(self) -> Result[None, CommandInputValidationError]:
        """Validate command input values."""

    @abc.abstractmethod
    def execute(
        self,
        write_ops_registry: UseCaseRegistry[Any],
    ) -> Result[Any, UseCaseExecutionError]:
        """Workflow execution command to complete the use case."""
