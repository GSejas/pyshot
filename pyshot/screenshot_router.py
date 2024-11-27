from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from playwright.sync_api import sync_playwright
from io import BytesIO
from fastapi.responses import StreamingResponse
import os
import uuid
from fastapi import FastAPI, HTTPException, Query, UploadFile, File

app = FastAPI()

# Directory to save screenshots
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

@app.post("/take")
async def take_screenshot(
    url: str = Query(..., description="The website to screenshot."),
    waitUntil: str = Query("load", description="Wait until event."),
    blockPopups: bool = Query(True, description="Block popups."),
    blockCookieBanners: bool = Query(True, description="Block cookie banners."),
    viewportDevice: str = Query(None, description="Viewport device."),
    viewportWidth: int = Query(1280, description="Viewport width."),
    viewportHeight: int = Query(720, description="Viewport height."),
    deviceScaleFactor: int = Query(1, ge=1, le=5, description="Device scale factor.")
):
    """
    Takes a screenshot of the specified URL with the given parameters.

    Args:
        url (str): The website to screenshot.
        waitUntil (str): Wait until event.
        blockPopups (bool): Block popups.
        blockCookieBanners (bool): Block cookie banners.
        viewportDevice (str): Viewport device.
        viewportWidth (int): Viewport width.
        viewportHeight (int): Viewport height.
        deviceScaleFactor (int): Device scale factor.

    Returns:
        dict: A dictionary containing the screenshot ID.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": viewportWidth, "height": viewportHeight, "deviceScaleFactor": deviceScaleFactor}
        )

        # Block popups and cookie banners if specified
        if blockPopups:
            page.route("**/*", lambda route, request: route.abort() if request.resource_type == "popup" else route.continue_())
        if blockCookieBanners:
            page.evaluate_on_new_document("""
                (() => {
                    const style = document.createElement('style');
                    style.type = 'text/css';
                    style.innerHTML = '.cookie-banner { display: none !important; }';
                    document.head.appendChild(style);
                })();
            """)

        try:
            page.goto(url, wait_until=waitUntil, timeout=10000)
            screenshot_buffer = page.screenshot(full_page=True)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error capturing screenshot: {str(e)}")
        finally:
            browser.close()

    # Save screenshot with a unique ID
    screenshot_id = str(uuid.uuid4())
    screenshot_path = os.path.join(SCREENSHOT_DIR, f"{screenshot_id}.png")
    with open(screenshot_path, "wb") as f:
        f.write(screenshot_buffer)

    return {"screenshot_id": screenshot_id}

@app.get("/screenshot/{screenshot_id}")
async def get_screenshot(screenshot_id: str):
    """
    Retrieves the screenshot by ID.

    Args:
        screenshot_id (str): The ID of the screenshot.

    Returns:
        FileResponse: The screenshot file.
    """
    screenshot_path = os.path.join(SCREENSHOT_DIR, f"{screenshot_id}.png")
    if not os.path.exists(screenshot_path):
        raise HTTPException(status_code=404, detail="Screenshot not found")

    return FileResponse(screenshot_path, media_type="image/png")
