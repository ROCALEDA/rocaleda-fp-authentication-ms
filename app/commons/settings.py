from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    users_ms: str
    secret_key: str
    algorithm: str


settings = Settings()
