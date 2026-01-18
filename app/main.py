import logging

from fastapi import FastAPI, status

from config import setting
from app.api.routes import orders
from app.logger_config import setup_logging


setup_logging(log_level=setting.logger.level)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=setting.api_setting.title,
    description=setting.api_setting.description,
    version=setting.api_setting.version,
    docs_url=setting.api_setting.docs_url,
    redoc_url=setting.api_setting.redoc_url
)

app.include_router(orders.router)


# можно использовать инициализацию БД / проверку...
# from app.init_db import init_db_with_admin


# @app.on_event("startup")
# async def startup_event():
#     """
#     Инициализация БД при запуске приложения.
#     Создает все таблицы и административного пользователя.
#     """
#     logger.info("Запуск приложения: инициализация базы данных...")
#     try:
#         init_db_with_admin()
#         logger.info("Инициализация базы данных завершена успешно!")
#     except Exception as e:
#         logger.error(f"Ошибка при инициализации базы данных: {e}", exc_info=True)
#         raise


@app.get("/")
def root():
    """
    Корневой endpoint API.
    """
    return {
        "title": setting.api_setting.title,
        "version": setting.api_setting.version,
        "docs": setting.api_setting.docs_url,
        "redoc": setting.api_setting.redoc_url
    }


@app.get("/health")
def health_check():
    """
    Проверка здоровья сервиса.
    """
    return {"status": "ok", "service": "order-management-api"}
