from pydantic import BaseSettings


class Settings(BaseSettings):
    postgres_host: str
    postgres_database: str
    postgres_user: str
    postgres_password: str
    jose_jwt_secret_key: str
    algorithm: str
    access_token_expire_minutes: str

    class Config:
        env_file = ".env"


settings = Settings()
