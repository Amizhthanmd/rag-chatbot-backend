from pydantic_settings import BaseSettings

#TODO Change in production
class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./databases/users.db"
    SECRET_KEY: str = "ABC@123"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 168  #7 days

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
