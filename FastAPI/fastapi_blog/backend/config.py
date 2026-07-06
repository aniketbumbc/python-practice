from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8"
    )

    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_mins: int = 20
    database_url: str

    max_upload_size_byt:int = 5* 1024 * 1024
    reset_token_expire_minutes: int = 10

    mail_server:str = "localhost"
    mail_port: int = 587
    mail_username: str = ""
    mail_password: SecretStr = SecretStr("")
    mail_from:str = "noreplay@gmail.com"
    mail_use_tls:bool = True

    frontend_url:str = "http://localhost:8000"
    supabase_url:str
    supabase_key:SecretStr
    supabase_bucket: str

settings = Settings()

