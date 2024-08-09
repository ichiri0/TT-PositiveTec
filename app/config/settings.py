from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=True,
    )

    # Переменные окружения
    ACTOR_1_URL: str
    ACTOR_2_URL: str
    DEBUG: bool

settings = Settings()
print(f"Актёр 1: {settings.ACTOR_1_URL}")
print(f"Актёр 2: {settings.ACTOR_2_URL}")

if settings.DEBUG:
    print("Активирован режим отладки")