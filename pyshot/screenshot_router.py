from fastapi import Depends, FastAPI, Query, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from playwright.sync_api import sync_playwright
from io import BytesIO
from fastapi.responses import StreamingResponse
import os
import uuid
from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from datetime import datetime
import asyncio
from .database import get_db
from .models import Screenshot
from .repo import ScreenshotRepo
from .utils.screenshot_utils import take_screenshot_util

app = FastAPI()

# Ensure the event loop policy is set to ProactorEventLoop on Windows
if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Directory to save screenshots
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


@app.post("/take")
def take_screenshot(
    url: str = Query(..., description="The website to screenshot."),
    waitUntil: str = Query("load", description="Wait until event."),
    blockPopups: bool = Query(True, description="Block popups."),
    blockCookieBanners: bool = Query(True, description="Block cookie banners."),
    viewportDevice: str = Query(None, description="Viewport device."),
    viewportWidth: int = Query(1280, description="Viewport width."),
    viewportHeight: int = Query(720, description="Viewport height."),
    deviceScaleFactor: int = Query(1, ge=1, le=5, description="Device scale factor."),
    fullPage: bool = Query(True, description="Capture full page."),
    db = Depends(get_db)
):
    """
    Takes a screenshot of the specified URL with the given parameters.

    Args:
        url (str): The website to screenshot.
        waitUntil (str): Wait until event. Options are "load", "domcontentloaded", "networkidle".
        blockPopups (bool): Block popups. Default is True.
        blockCookieBanners (bool): Block cookie banners. Default is True.
        viewportDevice (str): Viewport device. If specified, overrides viewportWidth and viewportHeight.
        viewportWidth (int): Viewport width in pixels. Default is 1280.
        viewportHeight (int): Viewport height in pixels. Default is 720.
        deviceScaleFactor (int): Device scale factor.

    Returns:
        dict: A dictionary containing the screenshot ID.
    """
    screenshot_id, screenshot_filename = take_screenshot_util(
        url, waitUntil, blockPopups, blockCookieBanners, viewportDevice, viewportWidth, viewportHeight, deviceScaleFactor, fullPage
    )

    # Save screenshot metadata to the database
    screenshot_db = ScreenshotRepo(db)
    screenshot = Screenshot(id=screenshot_id, filename=screenshot_filename, timestamp=datetime.utcnow())
    screenshot_db.add_screenshot(screenshot)

    return {"screenshot_id": screenshot_id, "filename": screenshot_filename}

@app.get("/screenshot/{screenshot_id}")
async def get_screenshot(
            screenshot_id: str,
            db = Depends(get_db)
        ):
    """
    Retrieves the screenshot by ID.

    Args:
        screenshot_id (str): The ID of the screenshot.

    Returns:
        FileResponse: The screenshot file.
    """
    screenshot_db = ScreenshotRepo(db)
    screenshot = screenshot_db.get_screenshot(screenshot_id)
    if not screenshot:
        raise HTTPException(status_code=404, detail="Screenshot not found")
    screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot.filename)
    return FileResponse(screenshot_path, media_type="image/png")

@app.get("/screenshots")
async def list_screenshots(
            db = Depends(get_db)
        ):
    """
    Lists all screenshots.

    Returns:
        list: A list of screenshot filenames.
    """
    screenshot_db = ScreenshotRepo(db)
    screenshots = screenshot_db.list_screenshots()
    return {"screenshots": [{"id": s.id, "filename": s.filename, "timestamp": s.timestamp} for s in screenshots]}
