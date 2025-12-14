import json
from datetime import datetime

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from config import pg_database_url, log_level
from models import *
from logs import Logs


class Application:
    def __init__(self):
        self.__engine = create_async_engine(
            pg_database_url,
            echo=log_level == "DEBUG",
            pool_size=5,
            max_overflow=10
        )
        self.__session_factory = async_sessionmaker(self.__engine)
        self.__logger = Logs('app').logger

    async def migrate_json(self) -> None:
        """
        Функция для загрузки json`а с данными в БД
        :return: None
        """
        async with self.__session_factory() as connection:
            with open("videos.json", 'r') as file:
                data = json.load(file)
                for values in data.values():
                    for videos in values:
                        video_id = videos.get('id')
                        await connection.execute(
                            insert(Videos).values(
                                id=video_id,
                                video_created_at=datetime.fromisoformat(videos.get('video_created_at')),
                                views_count=videos.get('views_count'),
                                likes_count=videos.get('likes_count'),
                                reports_count=videos.get('reports_count'),
                                comments_count=videos.get('comments_count'),
                                creator_id=videos.get('creator_id'),
                                created_at=datetime.fromisoformat(videos.get('created_at'))).on_conflict_do_nothing()
                        )
                        for snapshots in videos.get('snapshots'):
                            await connection.execute(
                                insert(Snapshots).values(
                                    id=snapshots.get('id'),
                                    video_id=video_id,
                                    views_count=snapshots.get('views_count'),
                                    likes_count=snapshots.get('likes_count'),
                                    reports_count=snapshots.get('reports_count'),
                                    comments_count=snapshots.get('comments_count'),
                                    delta_views_count=snapshots.get('delta_views_count'),
                                    delta_likes_count=snapshots.get('delta_likes_count'),
                                    delta_reports_count=snapshots.get('delta_reports_count'),
                                    delta_comments_count=snapshots.get('delta_comments_count'),
                                    created_at=datetime.fromisoformat(snapshots.get('created_at'))
                                ).on_conflict_do_nothing()
                            )

                await connection.commit()

    async def execute_query(self, query):
        async with self.__session_factory() as connection:
            return await connection.execute(text(query))
