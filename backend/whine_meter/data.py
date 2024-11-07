from datetime import datetime

from pydantic import BaseModel

from whine_meter import model


class Chat(BaseModel):
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


class Message(BaseModel):
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


class User(BaseModel):
    id: int
    """ID пользователя"""
    username: str
    """Имя пользователя"""
    created_at: datetime
    """Дата создания"""
    updated_at: datetime
    """Дата обновления"""
    role: str
    """Роль"""

    @classmethod
    def from_model(cls, user: model.User):
        return cls(
            id=user.id, username=user.username, created_at=user.created_at, updated_at=user.updated_at, role=user.role
        )


class PartialUser(BaseModel):
    id: int
    username: str


class GenericChatIDParams(BaseModel):
    chat_id: int
