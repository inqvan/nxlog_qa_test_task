from dataclasses import dataclass, replace
from enum import StrEnum


@dataclass(frozen=True)
class Todo:
    title: str
    completed: bool = False

    def as_completed(self) -> "Todo":
        return replace(self, completed=True)


@dataclass(frozen=True)
class TodoTextCase:
    """One of the text kinds a todo title has to support. `name` becomes the
    pytest parameter id, `description` the Allure test title."""

    name: str
    description: str
    title: str


class TodoFilter(StrEnum):
    ALL = "#/"
    ACTIVE = "#/active"
    COMPLETED = "#/completed"

    @property
    def link_name(self) -> str:
        return self.name.capitalize()
