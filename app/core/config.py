from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Анализ рекламы"
    database_url: str
    logs_file_path_local: str
    logs_file_path_prod: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
