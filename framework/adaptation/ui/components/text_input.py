from playwright.sync_api import expect

import allure

from framework.adaptation.ui.components.base_component import BaseComponent
from framework.execution.artifact_attachment import attach_step_screenshot


class TextInput(BaseComponent):

    def fill(self, text: str) -> None:
        with allure.step(f"Fill {self.component_type} '{self.name}' with '{text}'"):
            self.locator.fill(text)

    def press(self, key: str) -> None:
        with allure.step(f"Press '{key}' in {self.component_type} '{self.name}'"):
            self.locator.press(key)
            attach_step_screenshot(self.locator.page, f"After pressing '{key}' in '{self.name}'")

    def fill_and_submit(self, text: str) -> None:
        """The TodoMVC input has no submit button — Enter commits the value."""
        self.fill(text)
        self.press("Enter")

    def should_be_empty(self) -> None:
        with allure.step(f"Verify {self.component_type} '{self.name}' is empty"):
            self.should_have_value("")

    def should_have_value(self, value: str) -> None:
        with allure.step(f"Verify {self.component_type} '{self.name}' has value '{value}'"):
            expect(self.locator).to_have_value(value)
