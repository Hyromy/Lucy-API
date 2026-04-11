from pydantic import (
    Field,
    field_validator,
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from typing import (
    List,
    Optional,
    Union,
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_empty=True,
    )

    PRODUCTION: bool = False
    DJANGO_SECRET_KEY: str = Field(default="insecure-secret")

    HOSTS: Union[List[str], str] = Field(default=["*"])
    CORS_ALLOWED: Union[List[str], str] = Field(default=[])
    CSRF_TRUSTED: Union[List[str], str] = Field(default=[])

    PG_DB: Optional[str] = None
    PG_USER: Optional[str] = None
    PG_PASS: Optional[str] = None
    PG_HOST: str = "localhost"
    PG_PORT: int = 5432

    DISCORD_CLIENT_ID: Optional[str] = Field(default="")
    DISCORD_CLIENT_SECRET: Optional[str] = Field(default="")
    DISCORD_REDIRECT_URI: Optional[str] = Field(default="")

    @property
    def is_debug(self) -> bool:
        return not self.PRODUCTION

    @field_validator("HOSTS", "CORS_ALLOWED", "CSRF_TRUSTED", mode="before")
    @classmethod
    def assemble_list(cls, v: any, info) -> List[str]:
        if isinstance(v, str):
            if not v.strip():
                return ["*"] if info.field_name == "HOSTS" else []
            return [item.strip() for item in v.split(",")]
        return v or []

    @field_validator("DJANGO_SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str, info) -> str:
        if not info.data.get("PRODUCTION"):
            return v
        if v == "insecure-secret":
            raise ValueError("DJANGO_SECRET_KEY must be set in production")
        return v

    @field_validator("PG_DB", "PG_USER", "PG_PASS")
    @classmethod
    def validate_db_creds(cls, v: Optional[str], info) -> Optional[str]:
        if info.data.get("PRODUCTION") and v is None:
            raise ValueError(f"{info.field_name} must be set in production")
        return v


config = Settings()
