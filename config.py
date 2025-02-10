from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_TOKEN: str
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()