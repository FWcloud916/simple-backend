""" App Environment Configuration """
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Required environment variables"""

    APP_URL: str = Field("localhost")
    APP_ENV: str = Field("development")
    REGISTER_WHITELIST: bool = Field(False)
    EMAIL_ENABLED: bool = Field(False)
    EMAIL_CONFIRMATION_REQUIRED: bool = Field(False)
    EMAIL_CONFIRM_TOKEN_EXPIRE_MINUTES: int = Field(300)
    RESET_PASSWORD_TOKEN_EXPIRE_MINUTES: int = Field(300)
    POSTGRES_SERVER: str = Field("localhost")
    POSTGRES_USER: str = Field("backend")
    POSTGRES_PASSWORD: str = Field(
        "14b8991c57d7b835f880acb316485a48e8792304eff78debe66d7e16032051d9"
    )
    POSTGRES_DB: str = Field("app")
    SECRET_KEY: str = Field("14b8991c57d7b835f880acb316485a48e8792304eff78debe66d7e16032051d9")
    ALGORITHM: str = Field("HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(2880)
    DOCS_USERNAME: str = Field("admin")
    DOCS_PASSWORD: str = Field("admin")


settings = Settings()
