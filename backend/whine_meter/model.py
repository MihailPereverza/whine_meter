from datetime import datetime

from sqlalchemy import inspect, ForeignKey, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    def __repr__(self):
        fields_arr = [f"addr={id(self)}"]
        fields_arr.extend(f"{k}={getattr(self, k, None)}" for k in inspect(self.__class__).columns.keys())
        fields = ", ".join(fields_arr)
        return f"{self.__class__.__name__}({fields})"


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True)
    """ID чата от телеги"""
    title: Mapped[str] = mapped_column()
    """Название чата"""
    type: Mapped[str] = mapped_column()
    """Тип чата"""
    created_at: Mapped[datetime] = mapped_column()
    """Дата создания"""
    updated_at: Mapped[datetime] = mapped_column()
    """Дата обновления"""


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    """ID сообщения"""
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    """ID чата"""
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    """ID пользователя"""
    whine_value: Mapped[float] = mapped_column()
    """фактор нытья от 0 до 1"""
    created_at: Mapped[datetime] = mapped_column()
    """Дата создания"""
    updated_at: Mapped[datetime] = mapped_column()
    """Дата обновления"""

    author: Mapped["User"] = relationship()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    """ID пользователя"""
    username: Mapped[str] = mapped_column()
    """Имя пользователя"""
    created_at: Mapped[datetime] = mapped_column()
    """Дата создания"""
    updated_at: Mapped[datetime] = mapped_column()
    """Дата обновления"""
    role: Mapped[str] = mapped_column()
    """Роль"""
