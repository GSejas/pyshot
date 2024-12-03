from fastapi import FastAPI
from .screenshot_router import router as screenshot_router
from .database import engine, Base

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the screenshot router
app.include_router(screenshot_router)