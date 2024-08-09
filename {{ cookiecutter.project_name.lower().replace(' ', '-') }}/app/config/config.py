import os
from pydantic import BaseSettings, Field
from typing import Dict, Any
import yaml
from pathlib import Path


def get_yaml_config_path(environment: str) -> Path:
    config_dir = Path(__file__).parent / "yaml"
    return config_dir / f"{environment}.yaml"


def yaml_config_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    encoding = settings.__config__.env_file_encoding
    environment = os.getenv("ENVIRONMENT", "dev")
    yaml_path = get_yaml_config_path(environment)

    if not yaml_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {yaml_path}")

    yaml_settings = yaml.safe_load(yaml_path.read_text(encoding))
    return deep_update_env_vars(yaml_settings)


def deep_update_env_vars(d: Dict[str, Any]) -> Dict[str, Any]:
    for k, v in d.items():
        if isinstance(v, dict):
            d[k] = deep_update_env_vars(v)
        elif isinstance(v, str) and v.startswith("${") and v.endswith("}"):
            env_var = v[2:-1]
            d[k] = os.getenv(env_var, v)
    return d


class DatabaseSettings(BaseSettings):
    url: str = Field(..., env="DATABASE_URL")
    pool_size: int = Field(default=10, env="DATABASE_POOL_SIZE")
    max_overflow: int = Field(default=20, env="DATABASE_MAX_OVERFLOW")
    max_connections: int = Field(default=10, env="DATABASE_MAX_CONNECTIONS")
    min_connections: int = Field(default=10, env="DATABASE_MIN_CONNECTIONS")


class APISettings(BaseSettings):
    title: str = "{{cookiecutter.project_name}}"
    version: str = "0.1.0"
    prefix: str = "/api"


class SecuritySettings(BaseSettings):
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


class ModelSettings(BaseSettings):
    model_path: str = Field(..., env="MODEL_PATH")
    model_name: str = Field(..., env="MODEL_NAME")
    input_example: str = Field(..., env="INPUT_EXAMPLE")


class Settings(BaseSettings):
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")
    profile_endpoints: bool = Field(default=False, env="PROFILE_ENDPOINTS")

    database: DatabaseSettings = DatabaseSettings()
    api: APISettings = APISettings()
    security: SecuritySettings = SecuritySettings()
    model: ModelSettings = ModelSettings()

    class Config:
        env_file = "dotenv/.env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"

        @classmethod
        def customise_sources(
                cls,
                init_settings,
                env_settings,
                file_secret_settings,
        ):
            """
            Cначала используются значения, переданные при инициализации.
            Затем значения из YAML файла.
            Затем значения из переменных окружения.
            Наконец, значения из файла секретов (если есть).
            """
            return (
                init_settings,
                yaml_config_settings_source,
                env_settings,
                file_secret_settings,
            )


settings = Settings()
