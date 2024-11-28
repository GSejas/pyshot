from fastapi import HTTPException
from playwright.sync_api import sync_playwright
import os
import uuid
from datetime import datetime

DEVICE_VIEWPORTS = {
    "iPhone 12": {"width": 390, "height": 844, "deviceScaleFactor": 3},
    "iPad Pro": {"width": 1024, "height": 1366, "deviceScaleFactor": 2},
    "Galaxy S21": {"width": 360, "height": 800, "deviceScaleFactor": 3},
    "Pixel 5": {"width": 393, "height": 851, "deviceScaleFactor": 3},
    "Surface Pro 7": {"width": 912, "height": 1368, "deviceScaleFactor": 2},
    "MacBook Pro 16": {"width": 1536, "height": 960, "deviceScaleFactor": 2},
    "Desktop 1080p": {"width": 1920, "height": 1080, "deviceScaleFactor": 1},
    # Add more devices as needed
}

def take_screenshot_util(
            url: str,
            waitUntil: str,
            blockPopups: bool,
            blockCookieBanners: bool,
            viewportDevice: str,
            viewportWidth: int,
            viewportHeight: int,
            deviceScaleFactor: int,
            fullPage: bool = True
        ):
    """
    Takes a screenshot of a webpage using Playwright.
    Args:
        url (str): The URL of the webpage to capture.
        waitUntil (str): The event to wait for before taking the screenshot (e.g., 'load', 'domcontentloaded').
        blockPopups (bool): Whether to block popups on the webpage.
        blockCookieBanners (bool): Whether to block cookie banners on the webpage.
        viewportDevice (str): The device viewport to use (e.g., 'iPhone 12'). If not in DEVICE_VIEWPORTS, custom dimensions will be used.
        viewportWidth (int): The width of the viewport if a custom device is used.
        viewportHeight (int): The height of the viewport if a custom device is used.
        deviceScaleFactor (int): The device scale factor if a custom device is used.
        fullPage (bool, optional): Whether to capture the full page. Defaults to True.
    Returns:
        tuple: A tuple containing the screenshot ID and the screenshot filename.
    Raises:
        HTTPException: If there is an error capturing the screenshot.
    """
    with sync_playwright() as p:
        if viewportDevice in DEVICE_VIEWPORTS:
            viewport = DEVICE_VIEWPORTS[viewportDevice]
        else:
            viewport = {"width": viewportWidth, "height": viewportHeight, "deviceScaleFactor": deviceScaleFactor}

        browser = p.chromium.launch()
        page = browser.new_page(viewport=viewport)

        # Block popups and cookie banners if specified
        if blockPopups:
            page.route("**/*", lambda route, request: route.abort() if request.resource_type == "popup" else route.continue_())
        
        # TODO: Review why this is faililng
        #   File "C:\Users\a-a984560\AppData\Local\Programs\Python\Python311\Lib\concurrent\futures\thread.py", line 58, in run
        #  result = self.fn(*self.args, **self.kwargs)
        #      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # File "C:\Users\a-a984560\Documents\pyshot-main\pyshot\screenshot_router.py", line 60, in take_screenshot
        #     page.evaluate_on_new_document("""
        #     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # AttributeError: 'Page' object has no attribute 'evaluate_on_new_document'
        # WARNING:  StatReload detected file change in 'pyshot\screenshot_router.py'. Reloading...
        # INFO:     Started server process [11212]
        # if blockCookieBanners:
        #     page.evaluate_on_new_document("""
        #         (() => {
        #             const style = document.createElement('style');
        #             style.type = 'text/css';
        #             style.innerHTML = '.cookie-banner { display: none !important; }';
        #             document.head.appendChild(style);
        #         })();
        #     """)

        
        try:
            page.goto(url, wait_until=waitUntil, timeout=10000)
            screenshot_buffer = page.screenshot(full_page=fullPage)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error capturing screenshot: {str(e)}")
        finally:
            browser.close()

    screenshot_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    screenshot_filename = f"{screenshot_id}_{timestamp}.png"
    screenshot_path = os.path.join("screenshots", screenshot_filename)
    with open(screenshot_path, "wb") as f:
        f.write(screenshot_buffer)

    return screenshot_id, screenshot_filename