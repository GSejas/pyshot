from sqlalchemy.orm import Session
from pyshot.models import Screenshot


class ScreenshotRepo:
    def __init__(self, db: Session):
        self.db = db

    def add_screenshot(self, screenshot):
        self.db.add(screenshot)
        self.db.commit()
        self.db.refresh(screenshot)
        return screenshot

    def get_screenshot(self, screenshot_id):
        return self.db.query(Screenshot).filter(Screenshot.id == screenshot_id).first()

    def list_screenshots(self):
        return self.db.query(Screenshot).all()

    def close(self):
        self.db.close()