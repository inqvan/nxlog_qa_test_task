import allure
import pytest

from framework.definition.actions.ui.todo_actions import TodoActions
from framework.definition.data.models import TodoTextCase
from framework.definition.data.test_data import TODO_TEXT_CASES
from framework.definition.data.todo_factory import TodoFactory

pytestmark = pytest.mark.ui


@allure.title("A new todo item can be added using {text_case.description}")
@pytest.mark.parametrize("text_case", TODO_TEXT_CASES, ids=lambda text_case: text_case.name)
def test_add_todo(todo_actions: TodoActions, todo_factory: TodoFactory, text_case: TodoTextCase):
    todo = todo_factory.todo_for_text_case(text_case)

    todo_actions.open_todo_list()
    todo_actions.add_todo(todo)

    todo_actions.should_show_exactly([todo])
    todo_actions.should_show_todo_as_active(todo)
    todo_actions.should_have_items_left(1)
    todo_actions.should_have_empty_new_todo_input()
