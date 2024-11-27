
import os
import pytest
from fastapi.testclient import TestClient
from pyshot.screenshot_router import app, SCREENSHOT_DIR

client = TestClient(app)


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


def test_integration_take_and_get_screenshot():
    # Take a screenshot
    response = client.post("/take", params={"url": "https://example.com"})
    assert response.status_code == 200
    screenshot_id = response.json()["screenshot_id"]

    # Retrieve the screenshot
    response = client.get(f"/screenshot/{screenshot_id}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"