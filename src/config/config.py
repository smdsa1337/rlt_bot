import os


app_name = os.getenv("APP_NAME")
log_level = os.getenv("LOG_LEVEL", "INFO")
bot_token = os.getenv("BOT_TOKEN")

llm_url = os.getenv("LLM_URL", "http://localhost:11434")
llm_model = os.getenv("LLM_MODEL")

pg_host = os.getenv("PG_HOST")
pg_port = int(os.getenv("PG_PORT"))
pg_user = os.getenv("PG_USER")
pg_password = os.getenv("PG_PASSWORD")
pg_dbname = os.getenv("PG_DBNAME")
pg_database_url = f'postgresql+asyncpg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_dbname}'
