from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    users_ms: str


settings = Settings()
