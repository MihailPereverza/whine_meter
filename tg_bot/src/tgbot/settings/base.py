from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    tg_bot_token: str = 'some_token'
    """Токен тг бота"""
    admin_ids: list[int] = []
    """ID аккаунтов админов"""
    debug_mode: bool = True
    """Режим отладки"""

    class Config:
        env_file = ".env"  # Укажите файл .env, если он используется
        env_file_encoding = 'utf-8'


settings = Settings()   # type: ignore
