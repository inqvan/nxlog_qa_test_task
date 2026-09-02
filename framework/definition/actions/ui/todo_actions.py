from collections.abc import Iterable

import allure

from framework.adaptation.ui.pages.todo_mvc_page import TodoMvcPage
from framework.definition.data.models import Todo, TodoFilter
from framework.execution.logging_configuration import configure_logging

logger = configure_logging(__name__)


class TodoActions:
    def __init__(self, todo_mvc_page: TodoMvcPage):
        self.todo_mvc_page = todo_mvc_page

    def open_todo_list(self) -> None:
        logger.info("Opening the TodoMVC todo list")
        self.todo_mvc_page.open()
        self.todo_mvc_page.should_show_no_todos()

    def add_todo(self, todo: Todo) -> None:
        logger.info(f"Adding todo '{todo.title}'")
        self.todo_mvc_page.add_todo(todo.title)

    def add_todos(self, todos: Iterable[Todo]) -> None:
        for todo in todos:
            self.add_todo(todo)

    def complete_todo(self, todo: Todo) -> None:
        logger.info(f"Marking todo '{todo.title}' as completed")
        self.todo_mvc_page.item(todo.title).mark_completed()

    def delete_todo(self, todo: Todo) -> None:
        logger.info(f"Deleting todo '{todo.title}'")
        self.todo_mvc_page.item(todo.title).delete()

    def show(self, todo_filter: TodoFilter) -> None:
        logger.info(f"Switching to the '{todo_filter.link_name}' view")
        with allure.step(f"Switch to the '{todo_filter.link_name}' view"):
            self.todo_mvc_page.select_filter(todo_filter.link_name)
            self.todo_mvc_page.should_have_url_ending_with(todo_filter.value)
            self.todo_mvc_page.should_have_selected_filter(todo_filter.link_name)

    def should_show_exactly(self, todos: Iterable[Todo]) -> None:
        titles = [todo.title for todo in todos]
        logger.info(f"Verifying the current view shows exactly {titles}")
        self.todo_mvc_page.should_show_titles(titles)

    def should_show_todo(self, todo: Todo) -> None:
        logger.info(f"Verifying todo '{todo.title}' is shown")
        self.todo_mvc_page.item(todo.title).should_be_visible()

    def should_not_show_todo(self, todo: Todo) -> None:
        logger.info(f"Verifying todo '{todo.title}' is not shown")
        self.todo_mvc_page.item(todo.title).should_not_be_visible()

    def should_show_todo_as_completed(self, todo: Todo) -> None:
        logger.info(f"Verifying todo '{todo.title}' is shown as completed")
        self.todo_mvc_page.item(todo.title).should_be_completed()

    def should_show_todo_as_active(self, todo: Todo) -> None:
        logger.info(f"Verifying todo '{todo.title}' is shown as active")
        self.todo_mvc_page.item(todo.title).should_not_be_completed()

    def should_not_show_todo_in_any_view(self, todo: Todo) -> None:
        logger.info(f"Verifying todo '{todo.title}' is gone from every view")
        with allure.step(f"Verify todo '{todo.title}' is gone from every view"):
            for todo_filter in TodoFilter:
                self.show(todo_filter)
                self.should_not_show_todo(todo)

    def should_have_empty_new_todo_input(self) -> None:
        logger.info("Verifying the new-todo input was reset after submitting")
        self.todo_mvc_page.should_have_empty_new_todo_input()

    def should_have_items_left(self, count: int) -> None:
        logger.info(f"Verifying the counter reports {count} item(s) left")
        self.todo_mvc_page.should_have_items_left(count)
