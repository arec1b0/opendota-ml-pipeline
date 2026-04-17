from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "OpenDota ML Pipeline"
    API_V1_STR: str = "/api/v1"
    OPENDOTA_API_BASE_URL: str = "https://api.opendota.com/api"
    OPENDOTA_API_KEY: str | None = None
    MLFLOW_TRACKING_URI: str = "http://localhost:5000"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()