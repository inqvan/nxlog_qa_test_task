from playwright.sync_api import expect

import allure

from framework.adaptation.ui.components.base_component import BaseComponent
from framework.execution.artifact_attachment import attach_step_screenshot


class Checkbox(BaseComponent):

    def check(self) -> None:
        with allure.step(f"Check {self.component_type} '{self.name}'"):
            self.locator.check()
            attach_step_screenshot(self.locator.page, f"After checking {self.component_type} '{self.name}'")

    def uncheck(self) -> None:
        with allure.step(f"Uncheck {self.component_type} '{self.name}'"):
            self.locator.uncheck()
            attach_step_screenshot(self.locator.page, f"After unchecking {self.component_type} '{self.name}'")

    def should_be_checked(self) -> None:
        with allure.step(f"Verify {self.component_type} '{self.name}' is checked"):
            expect(self.locator).to_be_checked()

    def should_not_be_checked(self) -> None:
        with allure.step(f"Verify {self.component_type} '{self.name}' is not checked"):
            expect(self.locator).not_to_be_checked()
