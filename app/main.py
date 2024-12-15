from fastapi import FastAPI
from app.api.endpoints import video_analysis
import os
import logging

app = FastAPI(title="Video and Audio Analysis API")

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Set the path to FFmpeg binary explicitly
os.environ["FFMPEG_BINARY"] = "/opt/homebrew/bin/ffmpeg"

# Add the FFmpeg directory to the PATH environment variable for subprocesses
os.environ["PATH"] = "/opt/homebrew/bin/ffmpeg:" + os.environ["PATH"]



# Include API routes
app.include_router(video_analysis.router, prefix="/api/video", tags=["Video Analysis"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Video and Audio Analysis API"}
