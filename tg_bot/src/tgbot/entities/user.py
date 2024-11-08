from dataclasses import dataclass
from datetime import datetime

# users_table = sa.Table(
#     'users',
#     metadata,
#     sa.Column('id', sa.BIGINT, nullable=False, primary_key=True),
#     sa.Column('username', sa.VARCHAR, nullable=False),
#     sa.Column('first_name', sa.VARCHAR, nullable=True),
#     sa.Column('last_name', sa.VARCHAR, nullable=True),
#     sa.Column('language_code', sa.VARCHAR, nullable=True),
#     sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
#     sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
#     sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True),
#     sa.Column('role', sa.VARCHAR, nullable=False),
# )


@dataclass(slots=True, kw_only=True)
class User:
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


@dataclass(slots=True, kw_only=True)
class PartialUser:
    id: int
    """ID пользователя"""
    username: str
    """Имя пользователя"""
