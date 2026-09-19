from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Analytics API Backend"
    database_url: str = "sqlite:///./analytics.db"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
