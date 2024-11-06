from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, kw_only=True)
class Message:
    id: int
    """ID сообщения"""
    chat_id: int
    """ID чата"""
    user_id: int
    """ID пользователя"""
    text: str
    """Текст сообщения"""
    created_at: datetime
    """Дата создания"""
    updated_at: datetime
    """Дата обновления"""
