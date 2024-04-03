from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Анализ рекламы"
    database_url: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
