import re
from pathlib import Path

import pytest
from playwright.sync_api import Browser, Page

from framework.adaptation.ui.pages.todo_mvc_page import TodoMvcPage
from framework.definition.actions.ui.todo_actions import TodoActions
from framework.definition.data.todo_factory import TodoFactory
from framework.definition.data.ui_settings import UiSettings
from framework.execution.allure_environment import write_environment_file
from framework.execution.artifact_attachment import attach_test_artifacts, configure_step_screenshots

ARTIFACT_DIRECTORY = Path("test-results")
RECORDING_DIMENSIONS = {"width": 1280, "height": 800}
ARTIFACT_DIRECTORY_STASH_KEY = pytest.StashKey[Path]()

CURSOR_OVERLAY_SCRIPT = """
(() => {
    const cursor = document.createElement('div');
    cursor.style.cssText =
        'position:fixed;top:0;left:0;width:16px;height:16px;margin:-8px 0 0 -8px;' +
        'background:rgba(255,0,0,0.7);border:2px solid white;border-radius:50%;' +
        'pointer-events:none;z-index:2147483647;box-shadow:0 0 4px rgba(0,0,0,0.6);';

    function attachCursor() {
        document.body.appendChild(cursor);
    }

    if (document.body) {
        attachCursor();
    } else {
        document.addEventListener('DOMContentLoaded', attachCursor);
    }

    document.addEventListener('mousemove', (event) => {
        cursor.style.left = event.clientX + 'px';
        cursor.style.top = event.clientY + 'px';
    }, true);
})();
"""


def slugify_test_name(test_name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", test_name)


@pytest.fixture(scope="session")
def settings() -> UiSettings:
    return UiSettings()


@pytest.fixture(scope="session", autouse=True)
def allure_environment_info(settings: UiSettings) -> None:
    write_environment_file(Path("allure-results"), {"Base_URL": settings.base_url, "Browser": "chromium"})


@pytest.fixture(scope="session", autouse=True)
def configure_screenshot_capture(settings: UiSettings) -> None:
    configure_step_screenshots(settings.capture_screenshots)


@pytest.fixture
def todo_factory() -> TodoFactory:
    return TodoFactory()


@pytest.fixture
def page(browser: Browser, request: pytest.FixtureRequest, settings: UiSettings) -> Page:
    """A fresh browser context per test. TodoMVC keeps its list in localStorage,
    so a new context is what guarantees an empty list — no teardown cleanup needed."""
    test_name_slug = slugify_test_name(request.node.name)
    artifact_directory = ARTIFACT_DIRECTORY / test_name_slug
    artifact_directory.mkdir(parents=True, exist_ok=True)
    request.node.stash[ARTIFACT_DIRECTORY_STASH_KEY] = artifact_directory

    context_arguments = {"viewport": RECORDING_DIMENSIONS}
    if settings.capture_video:
        context_arguments["record_video_dir"] = str(artifact_directory)
        context_arguments["record_video_size"] = RECORDING_DIMENSIONS

    context = browser.new_context(**context_arguments)
    context.add_init_script(CURSOR_OVERLAY_SCRIPT)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield context.new_page()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """Captures and attaches artifacts right after the test body runs (pass or
    fail), while the page/context are still open — not in the `page` fixture's
    teardown. Allure attributes attachments to whatever phase is active when
    `allure.attach` is called: doing this in fixture teardown buries the
    screenshot/video/trace in the report's "Tear Down" section, alongside
    unrelated fixture-finalizer noise, instead of the main test body."""
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    page = item.funcargs.get("page")
    settings = item.funcargs.get("settings")
    artifact_directory = item.stash.get(ARTIFACT_DIRECTORY_STASH_KEY, None)
    if page is None or settings is None or artifact_directory is None:
        return

    context = page.context

    screenshot_path = None
    if settings.capture_screenshots:
        screenshot_path = artifact_directory / "screenshot.png"
        page.screenshot(path=str(screenshot_path))

    trace_path = artifact_directory / "trace.zip"
    context.tracing.stop(path=str(trace_path))
    video = page.video
    context.close()
    video_path = Path(video.path()) if video is not None else None

    attach_test_artifacts(screenshot_path, trace_path, video_path)


@pytest.fixture
def todo_mvc_page(page: Page, settings: UiSettings) -> TodoMvcPage:
    return TodoMvcPage(page, settings.base_url)


@pytest.fixture
def todo_actions(todo_mvc_page: TodoMvcPage) -> TodoActions:
    return TodoActions(todo_mvc_page)
