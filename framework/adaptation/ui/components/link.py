from playwright.sync_api import expect

import allure

from framework.adaptation.ui.components.base_component import BaseComponent

SELECTED_FILTER_CLASS = "selected"


class Link(BaseComponent):

    def should_be_selected(self) -> None:
        with allure.step(f"Verify {self.component_type} '{self.name}' is the selected filter"):
            expect(self.locator).to_have_class(SELECTED_FILTER_CLASS)
