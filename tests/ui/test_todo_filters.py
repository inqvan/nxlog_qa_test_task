import allure
import pytest

from framework.definition.actions.ui.todo_actions import TodoActions
from framework.definition.data.models import TodoFilter
from framework.definition.data.todo_factory import TodoFactory

pytestmark = pytest.mark.ui


@allure.title("The Active filter shows only the todo items that are not completed")
def test_active_filter_shows_only_incomplete_todos(todo_actions: TodoActions, todo_factory: TodoFactory):
    active_todo, todo_to_complete = todo_factory.mixed_todos()

    todo_actions.open_todo_list()
    todo_actions.add_todos([active_todo, todo_to_complete])
    todo_actions.complete_todo(todo_to_complete)

    todo_actions.show(TodoFilter.ACTIVE)

    todo_actions.should_show_exactly([active_todo])
    todo_actions.should_show_todo_as_active(active_todo)
    todo_actions.should_not_show_todo(todo_to_complete)


@allure.title("The Completed filter shows only the todo items that have been marked as completed")
def test_completed_filter_shows_only_completed_todos(todo_actions: TodoActions, todo_factory: TodoFactory):
    active_todo, todo_to_complete = todo_factory.mixed_todos()

    todo_actions.open_todo_list()
    todo_actions.add_todos([active_todo, todo_to_complete])
    todo_actions.complete_todo(todo_to_complete)

    todo_actions.show(TodoFilter.COMPLETED)

    todo_actions.should_show_exactly([todo_to_complete.as_completed()])
    todo_actions.should_show_todo_as_completed(todo_to_complete)
    todo_actions.should_not_show_todo(active_todo)
