from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    DEBUG: bool = False
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    FRONTEND_URL: str

    class Config:
        env_file = ".env"

# Khởi tạo settings để sử dụng
settings = Settings()