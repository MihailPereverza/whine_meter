from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, kw_only=True)
class Chat:
    id: int
    """ID чата от телеги"""
    title: str
    """Название чата"""
    type: str
    """Тип чата"""
    created_at: datetime
    """Дата создания"""
    updated_at: datetime
    """Дата обновления"""
