
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

def test_take_screenshot():
    response = client.post("/take", params={"url": "https://example.com"})
    assert response.status_code == 200
    assert "screenshot_id" in response.json()

def test_get_screenshot():
    # First, take a screenshot to get a valid screenshot_id
    response = client.post("/take", params={"url": "https://example.com"})
    screenshot_id = response.json()["screenshot_id"]

    # Now, retrieve the screenshot using the screenshot_id
    response = client.get(f"/screenshot/{screenshot_id}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"

def test_get_screenshot_not_found():
    response = client.get("/screenshot/nonexistent_id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Screenshot not found"}