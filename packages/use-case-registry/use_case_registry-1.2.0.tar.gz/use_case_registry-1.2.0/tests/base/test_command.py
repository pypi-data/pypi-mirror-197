"""Tests for command."""
import pytest
from result import Err, Ok, Result

from use_case_registry import UseCaseRegistry
from use_case_registry.base import ICommand
from use_case_registry.errors import CommandInputValidationError, UseCaseExecutionError


class TestICommand:
    """Test definition for ICommand."""

    def test_cannot_be_instantiated(self) -> None:
        """ICommand is an interface an cannot be instantiated."""
        with pytest.raises(TypeError):
            ICommand()  # type:ignore[abstract]

    def test_interface_can_be_extendend(self) -> None:
        """Test interface can be extended."""

        class ConcreteCommand(ICommand):
            def __init__(self, name: str, last_name: str) -> None:
                """Construct concrete implementation."""
                self.name = name
                self.last_name = last_name

            def validate(self) -> Result[None, CommandInputValidationError]:
                """Validate input arguments are valid."""
                conditions = self.name.isascii() and self.last_name.isascii()
                if not conditions:
                    return Err(CommandInputValidationError())

                return Ok()

            def execute(
                self,
                write_ops_registry: UseCaseRegistry[str],
            ) -> Result[str, UseCaseExecutionError]:
                _ = write_ops_registry
                return Ok()

        command = ConcreteCommand(name="Tomas", last_name="Perez")
        command.validate()
        command.execute(write_ops_registry=UseCaseRegistry[str](max_length=10))
