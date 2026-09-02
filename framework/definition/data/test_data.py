from framework.definition.data.models import TodoTextCase

TODO_TEXT_CASES = (
    TodoTextCase(
        name="english_text",
        description="English text",
        title="Buy milk on the way home",
    ),
    TodoTextCase(
        name="non_english_characters",
        description="non-English characters",
        title="Купить молоко по дороге домой",
    ),
    TodoTextCase(
        name="text_with_numbers",
        description="text that includes numbers",
        title="Buy 2 litres of milk before 19:45",
    ),
)

TODO_TO_COMPLETE_TITLE = "Submit the automation test task"
TODO_TO_DELETE_TITLE = "Cancel the unused subscription"
TODO_TO_KEEP_TITLE = "Prepare the release notes"
