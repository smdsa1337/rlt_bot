import re
import asyncio
import requests

from aiogram import Bot, Dispatcher
from aiogram.types import Message

from logs import Logs
from app import Application
from config import bot_token, llm_url, llm_model


bot = Bot(token=bot_token)
dp = Dispatcher()
proc = Application()
logger = Logs('srv').logger

@dp.message()
async def check_db(message: Message):
    answer = requests.post(f'{llm_url}/api/chat', json={
        'model': llm_model,
        'messages': [{
            'role': 'user',
            'content': f"""
                {message.text}
                Составь 1 SQL-запрос строго с запросом выше с явным указанием схем, согласно этим DDL таблиц, где videos это таблица с видео, а snapshots это почасовые замеры по одному видео

                CREATE TABLE rlt_bot.videos (
                    id uuid DEFAULT uuid_generate_v4() NOT NULL,
                    video_created_at timestamptz NOT NULL,
                    views_count int8 DEFAULT '0'::bigint NOT NULL,
                    likes_count int8 DEFAULT '0'::bigint NOT NULL,
                    reports_count int8 DEFAULT '0'::bigint NOT NULL,
                    comments_count int8 DEFAULT '0'::bigint NOT NULL,
                    creator_id text NOT NULL,
                    created_at timestamptz DEFAULT now() NOT NULL,
                    updated_at timestamptz DEFAULT now() NOT NULL,
                    CONSTRAINT videos_pkey PRIMARY KEY (id)
                );

                CREATE TABLE rlt_bot.snapshots (
                    id uuid DEFAULT uuid_generate_v4() NOT NULL,
                    video_id uuid NOT NULL,
                    views_count int8 DEFAULT '0'::bigint NOT NULL,
                    likes_count int8 DEFAULT '0'::bigint NOT NULL,
                    reports_count int8 DEFAULT '0'::bigint NOT NULL,
                    comments_count int8 DEFAULT '0'::bigint NOT NULL,
                    delta_views_count int8 DEFAULT '0'::bigint NOT NULL,
                    delta_likes_count int8 DEFAULT '0'::bigint NOT NULL,
                    delta_reports_count int8 DEFAULT '0'::bigint NOT NULL,
                    delta_comments_count int8 DEFAULT '0'::bigint NOT NULL,
                    created_at timestamptz DEFAULT now() NOT NULL,
                    updated_at timestamptz DEFAULT now() NOT NULL,
                    CONSTRAINT snapshots_pkey PRIMARY KEY (id),
                    CONSTRAINT video_snapshots_fkey FOREIGN KEY (video_id) REFERENCES rlt_bot.videos(id) ON DELETE CASCADE);
            """}
        ],
        'stream': False
    })

    sql = answer.json().get('message').get('content')
    logger.debug(f'Ответ LLM: {sql}')

    pattern_1 = r'```sql\s*(.*?)\s*```'
    pattern_2 = r'```\s*(.*?)\s*```'
    queries = [re.findall(pattern_1, sql, re.DOTALL), re.findall(pattern_2, sql, re.DOTALL)]
    try:
        query = queries[0][0]
    except IndexError:
        query = queries[1][0]
    logger.debug(f'SQL-запрос: {query}')

    answer = await proc.execute_query(query)
    answer = answer.fetchone()[0]
    logger.debug(f'Ответ БД: {answer}')

    if answer is None:
        answer = 0
    await message.answer(f'{answer}')


async def start() -> None:
    """
    Функция для запуска работы бота
    :return: None
    """
    logger.info('Миграция данных')
    await proc.migrate_json()
    logger.info('Бот начал свою работу')
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(start())

