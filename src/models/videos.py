import uuid

from sqlmodel import SQLModel, Field
from sqlalchemy import func, Column, DateTime
from sqlalchemy.dialects.postgresql import BIGINT, TEXT


class Videos(SQLModel, table=True):
    __tablename__ = 'videos'
    __table_args__ = ({'schema': 'rlt_bot'})

    id: uuid.UUID = Field(primary_key=True, sa_column_kwargs={
        'server_default': func.uuid_generate_v4()
    })
    video_created_at: str = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    views_count: int = Field(sa_column=Column(BIGINT, server_default='0', nullable=False))
    likes_count: int = Field(sa_column=Column(BIGINT, server_default='0', nullable=False))
    reports_count: int = Field(sa_column=Column(BIGINT, server_default='0', nullable=False))
    comments_count: int = Field(sa_column=Column(BIGINT, server_default='0', nullable=False))
    creator_id: str = Field(sa_column=Column(TEXT, nullable=False))
    created_at: str = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: str = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
