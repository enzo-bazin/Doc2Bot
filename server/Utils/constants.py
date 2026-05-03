from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Base directories
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    SERVER_DIR: Path = BASE_DIR / "server"
    DATABASE_DIR: Path = SERVER_DIR / "Database" / "db"
    UPLOAD_DIR: Path = SERVER_DIR / "Upload"
    
    # Database Paths
    USER_DB_PATH: Path = DATABASE_DIR / "users.db"
    SESSION_DB_PATH: Path = DATABASE_DIR / "session.db"
    
    # Security
    TOKEN_KEY: str = "default_secret_key_change_me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # App Config
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Initialize settings
settings = Settings()

# Ensure directories exist
settings.DATABASE_DIR.mkdir(parents=True, exist_ok=True)
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
