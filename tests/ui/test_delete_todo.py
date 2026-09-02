import allure
import pytest

from framework.definition.actions.ui.todo_actions import TodoActions
from framework.definition.data.models import TodoFilter
from framework.definition.data.todo_factory import TodoFactory

pytestmark = pytest.mark.ui


@allure.title("A deleted todo item no longer appears in any view")
def test_deleted_todo_disappears_from_every_view(todo_actions: TodoActions, todo_factory: TodoFactory):
    todo_to_delete = todo_factory.todo_to_delete()
    todo_to_keep = todo_factory.todo_to_keep()

    todo_actions.open_todo_list()
    todo_actions.add_todos([todo_to_delete, todo_to_keep])

    todo_actions.delete_todo(todo_to_delete)

    todo_actions.should_show_exactly([todo_to_keep])
    todo_actions.should_have_items_left(1)
    todo_actions.should_not_show_todo_in_any_view(todo_to_delete)

    todo_actions.show(TodoFilter.ALL)
    todo_actions.should_show_todo(todo_to_keep)
