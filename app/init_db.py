"""
Скрипт инициализации базы данных.
Создает все таблицы согласно схеме БД и создает административного пользователя.
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from app.database import engine, Base, SessionLocal
from app.models import (
    Client, Category, Product, Order, OrderItem,
    OrderStatus, OrderPriority, PaymentMethod, PaymentStatus,
    DeliveryType, OrderSource, Payment, OrderStatusHistory, OrderComment
)
import time
import logging



logger = logging.getLogger(__name__)


def wait_for_db(max_retries=30, delay=2):
    """
    Ожидает готовности базы данных.
    """
    from sqlalchemy import text
    logger.info("Проверка готовности базы данных...")
    for i in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("База данных готова к подключению!")
            return True
        except OperationalError as e:
            if i < max_retries - 1:
                logger.warning(f"Ожидание базы данных... ({i+1}/{max_retries}) - {str(e)}")
                time.sleep(delay)
            else:
                logger.error(f"Не удалось подключиться к базе данных после {max_retries} попыток: {e}")
                raise
    return False


def init_database():
    """
    Создает все таблицы в БД согласно схеме.
    """
    logger.info("Начало создания таблиц в базе данных...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Все таблицы успешно созданы в базе данных!")
    except Exception as e:
        logger.error(f"Ошибка при создании таблиц: {e}", exc_info=True)
        raise


def create_admin_user(db: Session):
    """
    Создает административного пользователя в таблице clients.
    Если администратор уже существует, пропускает создание.
    """
    logger.info("Проверка существования административного пользователя...")
    admin = db.query(Client).filter(Client.name == "Администратор").first()
    
    if admin:
        logger.info(f"Административный пользователь уже существует (ID: {admin.id}, имя: {admin.name})")
        return admin
    
    logger.info("Создание нового административного пользователя...")
    admin = Client(
        name="Администратор",
        address="Системный пользователь"
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    logger.info(f"Административный пользователь успешно создан (ID: {admin.id}, имя: {admin.name})")
    return admin


def init_db_with_admin():
    """
    Полная инициализация: создание таблиц и администратора.
    """
    logger.info("Начало инициализации базы данных с администратором...")
    try:
        wait_for_db()
        
        init_database()
        
        db = SessionLocal()
        try:
            create_admin_user(db)
        except Exception as e:
            logger.error(f"Ошибка при создании администратора: {e}", exc_info=True)
            raise
        finally:
            db.close()
        
        logger.info("Инициализация базы данных завершена успешно!")
    except Exception as e:
        logger.critical(f"Критическая ошибка при инициализации БД: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    init_db_with_admin()
