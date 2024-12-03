import os
import pytest
import requests
# import docker
from time import sleep
from subprocess import Popen, PIPE

DOCKER_COMPOSE_FILE = "docker-compose.yml"
DOCKER_PORT = 8000
BASE_URL = f"http://localhost:{DOCKER_PORT}"

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Assume Docker service is already running
    sleep(1)  # Give the container some time to ensure it's ready

    yield

    # No teardown needed as Docker service is managed externally

def test_take_screenshot():
    response = requests.post(f"{BASE_URL}/take", params={"url": "https://example.com"})
    assert response.status_code == 200
    assert "screenshot_id" in response.json()

def test_get_screenshot():
    response = requests.post(f"{BASE_URL}/take", params={"url": "https://example.com"})
    screenshot_id = response.json()["screenshot_id"]

    response = requests.get(f"{BASE_URL}/screenshot/{screenshot_id}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"

def test_get_screenshot_not_found():
    response = requests.get(f"{BASE_URL}/screenshot/nonexistent_id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Screenshot not found"}