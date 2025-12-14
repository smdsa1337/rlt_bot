import uuid

from sqlmodel import SQLModel, Field
from sqlalchemy import func, Column, DateTime, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import BIGINT, UUID


class Snapshots(SQLModel, table=True):
    __tablename__ = 'snapshots'
    __table_args__ = (
        ForeignKeyConstraint(['video_id'], ['rlt_bot.videos.id'], ondelete='CASCADE',
                             name='video_snapshots_fkey'),
        {'schema': 'rlt_bot'})

    id: uuid.UUID = Field(primary_key=True, sa_column_kwargs={
        'server_default': func.uuid_generate_v4()
    })
    video_id: uuid.UUID = Field(sa_column=Column(UUID, nullable=False))
    views_count: int = Field(sa_column=Column(BIGINT, server_default='0', nullable=False))
    likes_count: int = Field(sa_column=Column(BIGINT, server_default='0', nullable=False))
    reports_count: int = Field(sa_column=Column(BIGINT, server_default='0', nullable=False))
    comments_count: int = Field(sa_column=Column(BIGINT, server_default='0', nullable=False))
    delta_views_count: int = Field(sa_column=Column(BIGINT, server_default='0', nullable=False))
    delta_likes_count: int = Field(sa_column=Column(BIGINT, server_default='0', nullable=False))
    delta_reports_count: int = Field(sa_column=Column(BIGINT, server_default='0', nullable=False))
    delta_comments_count: int = Field(sa_column=Column(BIGINT, server_default='0', nullable=False))
    created_at: str = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: str = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
