# NXLog Test Task

[![Allure Report](https://img.shields.io/badge/Allure-Latest%20Report-blue?style=for-the-badge)](https://inqvan.github.io/nxlog_qa_test_task/)

**[▶ Video Example of a Deletion Test](https://inqvan.github.io/nxlog_qa_test_task/data/attachments/29351ec73d7c0a26.webm)**

Automated UI tests for https://demo.playwright.dev/todomvc/#/ — Playwright + Pytest + Allure, managed with uv.

## Setup and run

```bash
uv sync
uv run playwright install chromium
cp .env.example .env   # BASE_URL, CAPTURE_SCREENSHOTS, CAPTURE_VIDEO
uv run pytest tests/ui
```

To view the report locally:

```bash
allure serve allure-results
```

## What the tests cover

| Requirement | Test |
| --- | --- |
| A new todo item can be added using English text | `test_add_todo[english_text]` |
| A new todo item can be added using non-English characters | `test_add_todo[non_english_characters]` |
| A new todo item can be added that includes numbers | `test_add_todo[text_with_numbers]` |
| A todo item can be marked as completed and appears correctly in the "Completed" view | `test_completed_todo_appears_in_the_completed_view` |
| A todo item can be deleted and no longer appears in any view | `test_deleted_todo_disappears_from_every_view` |
| The "Active" filter correctly shows only items that are not completed | `test_active_filter_shows_only_incomplete_todos` |
| The "Completed" filter correctly shows only items that have been marked as completed | `test_completed_filter_shows_only_completed_todos` |

Seven requirements, five test functions: the three "can be added" requirements differ only in the
input text, so they are one parametrized test rather than three copies.

The deletion test does not just check the current view — it walks All, Active and Completed and
asserts the item is absent from each of them, because "no longer appears in any view" is the actual
requirement. The filter tests assert the *exact* visible list, so an item leaking into the wrong
filter fails the test instead of passing unnoticed.

## Architecture

The framework follows the ISTQB test automation architecture:

```
framework/
  adaptation/   # the only layer that imports Playwright: components + pages
  definition/   # business language: actions, data, settings
  execution/    # logging, Allure environment, artifact attachment
tests/ui/       # test functions composing Definition-layer actions
```

* **Adaptation** — component-based page objects. `BaseComponent` gives every component
  `click`/`hover`/`should_be_visible`/`should_have_text`, an auto-generated Allure step name built
  from the component type and its name, and a screenshot after each click. `TodoItem` wraps one
  `<li>` with the vocabulary of the domain (`mark_completed`, `delete`, `should_be_completed`), so a
  test never touches a locator. All assertions use Playwright's auto-retrying `expect`.
* **Definition** — `TodoActions` speaks in todos and views, not in selectors, and holds no Playwright
  import at all. `TodoFactory` is the seam for future dynamic test-data provisioning; today it builds
  todos from constants. Settings come from `.env` through pydantic-settings.
* **Execution** — logging, the Allure `environment.properties`, and artifact attachment.

There is no API layer: TodoMVC is a front-end-only demo with nothing to call. The Adaptation layer is
structured so an `adaptation/api/` sibling can be added later without touching the Definition or
Execution layers.

**No cleanup fixtures.** TodoMVC stores its list in `localStorage`, and each test gets a fresh browser
context, so every test starts from an empty list by construction.

## Reporting

Screenshot, video and Playwright trace are attached to Allure for **every** test, not only failures.
They are captured in a `pytest_runtest_makereport` hookwrapper while the page is still open — doing
it in fixture teardown would file them under the report's "Tear Down" section instead of the test
body. A red cursor overlay is injected into every browser context so the recorded video shows where
the clicks land, and `--slowmo=1000` keeps that video readable.

CI runs the suite on every push to `main` and on manual dispatch, then publishes the Allure report to
GitHub Pages.

## What I would add with more time

* Reporting beyond Allure. An Allure report is useful, but the whole team does not always open it —
  the suite should also push metrics to something like Grafana.
* Cross-browser and multi-environment runs. Everything needed is already behind settings and the
  `browser` fixture; at this scale it would be premature optimisation.
* The remaining TodoMVC behaviour: editing an item, "Clear completed", "Mark all as complete",
  persistence across a reload, and the empty-input edge case.
* Quality-of-life tooling — a linter, a formatter and type checking in CI.
* Test data as a real concern. `TodoFactory` is deliberately the only place that mints todos, so
  moving to generated or API-seeded data later touches one file.
