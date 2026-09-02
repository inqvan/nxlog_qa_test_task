import re

from playwright.sync_api import Page, expect

import allure

from framework.adaptation.ui.components.link import Link
from framework.adaptation.ui.components.text_input import TextInput
from framework.adaptation.ui.components.todo_item import TodoItem

NEW_TODO_PLACEHOLDER = "What needs to be done?"


class TodoMvcPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url.rstrip("/")
        self.new_todo_input = TextInput(page.get_by_placeholder(NEW_TODO_PLACEHOLDER), "New todo")
        self.todo_items = page.get_by_test_id("todo-item")
        self.todo_titles = page.get_by_test_id("todo-title")
        self.todo_counter = page.get_by_test_id("todo-count")

    def open(self) -> None:
        with allure.step("Open the TodoMVC application"):
            self.page.goto(f"{self.base_url}/#/")
            self.new_todo_input.should_be_visible()

    def add_todo(self, title: str) -> None:
        with allure.step(f"Add todo '{title}'"):
            self.new_todo_input.fill_and_submit(title)

    def item(self, title: str) -> TodoItem:
        return TodoItem(self.todo_items.filter(has_text=title), f"Todo '{title}'")

    def filter_link(self, name: str) -> Link:
        return Link(self.page.get_by_role("link", name=name, exact=True), f"{name} filter")

    def select_filter(self, name: str) -> None:
        with allure.step(f"Select the '{name}' filter"):
            self.filter_link(name).click()

    def should_have_empty_new_todo_input(self) -> None:
        self.new_todo_input.should_be_empty()

    def should_show_titles(self, titles: list[str]) -> None:
        with allure.step(f"Verify the list shows exactly {titles}"):
            expect(self.todo_titles).to_have_text(titles)

    def should_show_no_todos(self) -> None:
        with allure.step("Verify the list is empty"):
            expect(self.todo_items).to_have_count(0)

    def should_have_items_left(self, count: int) -> None:
        with allure.step(f"Verify the counter reports {count} item(s) left"):
            expect(self.todo_counter).to_have_text(re.compile(rf"^{count} items? left$"))

    def should_have_selected_filter(self, name: str) -> None:
        self.filter_link(name).should_be_selected()

    def should_have_url_ending_with(self, fragment: str) -> None:
        with allure.step(f"Verify the URL ends with '{fragment}'"):
            expect(self.page).to_have_url(re.compile(rf"{re.escape(fragment)}$"))
