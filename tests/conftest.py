import os
import pytest
from pyshot import SCREENSHOT_DIR


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    """
    Setup and teardown fixture for tests.

    This fixture ensures that the screenshot directory exists before tests run,
    and cleans up the directory by removing all files after tests complete.

    Setup:
        - Creates the screenshot directory if it does not exist.

    Teardown:
        - Removes all files in the screenshot directory.

    Yields:
        None
    """
    # Setup: Ensure the screenshot directory exists
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    yield
    # Teardown: Clean up the screenshot directory
    for file in os.listdir(SCREENSHOT_DIR):
        file_path = os.path.join(SCREENSHOT_DIR, file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
