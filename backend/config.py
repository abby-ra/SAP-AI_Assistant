from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_env: str = os.getenv("APP_ENV", "dev")
    app_port: int = int(os.getenv("APP_PORT", "8000"))
    model_api_key: str = os.getenv("MODEL_API_KEY", "")
    db_engine: str = os.getenv("DB_ENGINE", "postgres")
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
    db_name: str = os.getenv("DB_NAME", "sap_ai_assistant")
    db_user: str = os.getenv("DB_USER", "")
    db_password: str = os.getenv("DB_PASSWORD", "")


settings = Settings()
