import allure
import pytest

from framework.definition.actions.ui.todo_actions import TodoActions
from framework.definition.data.models import TodoFilter
from framework.definition.data.todo_factory import TodoFactory

pytestmark = pytest.mark.ui


@allure.title("A todo item can be marked as completed and appears in the Completed view")
def test_completed_todo_appears_in_the_completed_view(todo_actions: TodoActions, todo_factory: TodoFactory):
    todo = todo_factory.todo_to_complete()

    todo_actions.open_todo_list()
    todo_actions.add_todo(todo)
    todo_actions.complete_todo(todo)

    todo_actions.should_show_todo_as_completed(todo)
    todo_actions.should_have_items_left(0)

    todo_actions.show(TodoFilter.COMPLETED)
    todo_actions.should_show_exactly([todo.as_completed()])
    todo_actions.should_show_todo_as_completed(todo)

    todo_actions.show(TodoFilter.ACTIVE)
    todo_actions.should_not_show_todo(todo)
