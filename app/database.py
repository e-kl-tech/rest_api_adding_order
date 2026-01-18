import logging
import os

from sys import exit

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings

from config import setting

load_dotenv()

logger = logging.getLogger(__name__)


database_url: str = setting.database.database_url


if "@" not in database_url:
    msg = "Не верная срока подключения"
    logger.error(msg)
    exit(1)

database_url = database_url
if not database_url.endswith("/orders_db"):
    url_parts = database_url.split("/")
    db_name = url_parts[-1] if url_parts else None
    if db_name and db_name != setting.database.name:
        msg = f"Имя базы данных в URL: '{db_name}', ожидается 'orders_db'"
        logger.warning(f"Имя базы данных в URL: '{db_name}', ожидается 'orders_db'")

db_url_parts = database_url.split("@")
try:
    engine = create_engine(
        database_url,
        pool_pre_ping=setting.engine.pool_pre_ping or 10,
        pool_size=setting.engine.pool_size or 10,
        max_overflow=setting.engine.max_overflow or 10,
        connect_args={
            "connect_timeout": setting.engine.connect_args.connect_timeout or 10
        }
    )
except Exception as e:
    logger.error("%s", e, exc_info=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
