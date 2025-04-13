from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    
    STATIC_PATH: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
