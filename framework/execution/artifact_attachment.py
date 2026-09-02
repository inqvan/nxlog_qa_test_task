from pathlib import Path

import allure
from playwright.sync_api import Page

step_screenshots_enabled = True


def configure_step_screenshots(enabled: bool) -> None:
    global step_screenshots_enabled
    step_screenshots_enabled = enabled


def attach_test_artifacts(screenshot_path: Path | None, trace_path: Path, video_path: Path | None) -> None:
    if screenshot_path is not None:
        allure.attach.file(str(screenshot_path), name="screenshot", attachment_type=allure.attachment_type.PNG)
    allure.attach.file(str(trace_path), name="trace", attachment_type=allure.attachment_type.ZIP)
    if video_path is not None and video_path.exists():
        allure.attach.file(str(video_path), name="video", attachment_type=allure.attachment_type.WEBM)


def attach_step_screenshot(page: Page, name: str) -> None:
    if not step_screenshots_enabled:
        return
    screenshot_bytes = page.screenshot()
    allure.attach(screenshot_bytes, name=name, attachment_type=allure.attachment_type.PNG)
