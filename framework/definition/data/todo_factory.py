from framework.definition.data.models import Todo, TodoTextCase
from framework.definition.data.test_data import (
    TODO_TO_COMPLETE_TITLE,
    TODO_TO_DELETE_TITLE,
    TODO_TO_KEEP_TITLE,
)


class TodoFactory:
    """The seam for future dynamic test-data provisioning (e.g. seeding todos
    through an API or through localStorage); today it builds them from constants."""

    def todo_for_text_case(self, text_case: TodoTextCase) -> Todo:
        return Todo(title=text_case.title)

    def todo_to_complete(self) -> Todo:
        return Todo(title=TODO_TO_COMPLETE_TITLE)

    def todo_to_delete(self) -> Todo:
        return Todo(title=TODO_TO_DELETE_TITLE)

    def todo_to_keep(self) -> Todo:
        return Todo(title=TODO_TO_KEEP_TITLE)

    def mixed_todos(self) -> tuple[Todo, Todo]:
        """A todo that stays active and a todo that gets completed — the pair the
        filter tests need."""
        return self.todo_to_keep(), self.todo_to_complete()
