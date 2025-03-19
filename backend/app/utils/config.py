from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "MedNLP API"
    api_version: str = "1.0.0"
    model_cache_time: int = 3600  # 1 hour
    
    class Config:
        env_file = ".env"

settings = Settings()