import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from .metadata import metadata

messages_table = sa.Table(
    'messages',
    metadata,
    sa.Column('id', sa.BIGINT, nullable=False, primary_key=True),
    sa.Column('chat_id', sa.BIGINT, nullable=False),
    sa.Column('user_id', sa.BIGINT, nullable=False),
    sa.Column('text', sa.TEXT, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('whine_value', sa.FLOAT, nullable=False),
    sa.Column('old_versions', JSONB, nullable=False),

    sa.ForeignKeyConstraint(['chat_id'], ['chats.id']),
    sa.ForeignKeyConstraint(['user_id'], ['users.id']),
)
