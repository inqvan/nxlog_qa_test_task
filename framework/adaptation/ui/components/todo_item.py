from playwright.sync_api import Locator, expect

import allure

from framework.adaptation.ui.components.base_component import BaseComponent
from framework.adaptation.ui.components.checkbox import Checkbox

COMPLETED_ITEM_CLASS = "completed"


class TodoItem(BaseComponent):
    def __init__(self, locator: Locator, name: str):
        super().__init__(locator, name)
        self.title_label = BaseComponent(locator.get_by_test_id("todo-title"), f"Title of '{name}'")
        self.toggle_checkbox = Checkbox(locator.get_by_role("checkbox", name="Toggle Todo"), f"Toggle of '{name}'")
        self.delete_button = BaseComponent(locator.get_by_role("button", name="Delete"), f"Delete button of '{name}'")

    def mark_completed(self) -> None:
        with allure.step(f"Mark {self.component_type} '{self.name}' as completed"):
            self.toggle_checkbox.check()

    def mark_active(self) -> None:
        with allure.step(f"Mark {self.component_type} '{self.name}' as active"):
            self.toggle_checkbox.uncheck()

    def delete(self) -> None:
        with allure.step(f"Delete {self.component_type} '{self.name}'"):
            # The delete button is revealed by CSS only while the item is hovered.
            self.hover()
            self.delete_button.click()

    def should_be_completed(self) -> None:
        with allure.step(f"Verify {self.component_type} '{self.name}' is completed"):
            expect(self.locator).to_have_class(COMPLETED_ITEM_CLASS)
            self.toggle_checkbox.should_be_checked()

    def should_not_be_completed(self) -> None:
        with allure.step(f"Verify {self.component_type} '{self.name}' is not completed"):
            expect(self.locator).not_to_have_class(COMPLETED_ITEM_CLASS)
            self.toggle_checkbox.should_not_be_checked()
