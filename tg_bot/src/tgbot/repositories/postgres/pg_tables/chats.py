import sqlalchemy as sa

from .metadata import metadata

chats_table = sa.Table(
    'chats',
    metadata,
    sa.Column('id', sa.BIGINT, nullable=False, primary_key=True),
    sa.Column('title', sa.VARCHAR, nullable=False),
    sa.Column('type', sa.VARCHAR, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
)
