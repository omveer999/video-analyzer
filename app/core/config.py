import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Secret keys
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-secret-key")

    # Database Configuration
    # DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    
    #FFMPEG PATH
    FFMPEG_PATH: str = os.getenv("FFMPEG_PATH", "/opt/homebrew/bin/ffmpeg")
    
    # OpenAI Key
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
     # OpenAI Key
    DEEPGRAM_API_KEY: str = os.getenv("DEEPGRAM_API_KEY", "")
    
     # OpenAI Key
    GOOGLE_PERSPECTIVE_API_KEY: str = os.getenv("GOOGLE_PERSPECTIVE_API_KEY", "")

    # Model Paths
    VIDEO_MODEL_PATH: str = os.getenv("VIDEO_MODEL_PATH", "models/video_model.h5")
    
        # Model Paths
    AUDIO_MODEL_PATH: str = os.getenv("AUDIO_MODEL_PATH", "models/audio_model.pt")


    class Config:
        env_file = ".env"

# Initialize settings instance
settings = Settings()
