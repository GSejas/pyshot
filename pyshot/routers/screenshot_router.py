
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Screenshot
from ..utils.screenshot_utils import take_screenshot_util
import os

router = APIRouter()

# Directory to save screenshots
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

@router.post("/take")
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
):
    screenshot_id, screenshot_filename = take_screenshot_util(
        url, waitUntil, blockPopups, blockCookieBanners, viewportDevice, viewportWidth, viewportHeight, deviceScaleFactor, fullPage
    )

    # Save screenshot metadata to the database
    db = SessionLocal()
    screenshot = Screenshot(id=screenshot_id, filename=screenshot_filename, timestamp=datetime.utcnow())
    db.add(screenshot)
    db.commit()
    db.refresh(screenshot)
    db.close()

    return {"screenshot_id": screenshot_id, "filename": screenshot_filename}

@router.get("/screenshot/{screenshot_id}")
async def get_screenshot(screenshot_id: str):
    db = SessionLocal()
    screenshot = db.query(Screenshot).filter(Screenshot.id == screenshot_id).first()
    db.close()
    if not screenshot:
        raise HTTPException(status_code=404, detail="Screenshot not found")
    screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot.filename)
    return FileResponse(screenshot_path, media_type="image/png")

@router.get("/screenshots")
async def list_screenshots():
    db = SessionLocal()
    screenshots = db.query(Screenshot).all()
    db.close()
    return {"screenshots": [{"id": s.id, "filename": s.filename, "timestamp": s.timestamp} for s in screenshots]}