import os
import pytest
from pyshot.screenshot_router import SCREENSHOT_DIR


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Setup: Ensure the screenshot directory exists
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    yield
    # Teardown: Clean up the screenshot directory
    for file in os.listdir(SCREENSHOT_DIR):
        file_path = os.path.join(SCREENSHOT_DIR, file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
