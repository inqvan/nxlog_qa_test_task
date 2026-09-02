from playwright.sync_api import Locator, expect

import allure

from framework.execution.artifact_attachment import attach_step_screenshot


class BaseComponent:
    def __init__(self, locator: Locator, name: str):
        self.locator = locator
        self.name = name

    @property
    def component_type(self) -> str:
        return type(self).__name__

    def click(self) -> None:
        with allure.step(f"Click {self.component_type} '{self.name}'"):
            self.locator.click()
            attach_step_screenshot(self.locator.page, f"After clicking {self.component_type} '{self.name}'")

    def hover(self) -> None:
        with allure.step(f"Hover over {self.component_type} '{self.name}'"):
            self.locator.hover()

    def should_be_visible(self) -> None:
        with allure.step(f"Verify {self.component_type} '{self.name}' is visible"):
            expect(self.locator).to_be_visible()

    def should_not_be_visible(self) -> None:
        with allure.step(f"Verify {self.component_type} '{self.name}' is not visible"):
            expect(self.locator).not_to_be_visible()

    def should_have_text(self, text: str) -> None:
        with allure.step(f"Verify {self.component_type} '{self.name}' has text '{text}'"):
            expect(self.locator).to_have_text(text)
