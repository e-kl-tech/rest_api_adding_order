import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import AddItemToOrderRequest, OrderItemResponse, ErrorResponse
from app.services import OrderService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post(
    "/add-item",
    response_model=OrderItemResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Заказ или товар не найдены"},
        400: {"model": ErrorResponse, "description": "Недостаточно товара на складе"},
    },
    summary="Добавить товар в заказ",
    description="""
    Добавляет товар в заказ по REST API.
    
    **Параметры:**
    - `order_id`: ID существующего заказа
    - `product_id`: ID товара из справочника номенклатуры
    - `quantity`: Количество товара для добавления (должно быть > 0)
    
    **Логика работы:**
    - Если товар уже присутствует в заказе, его количество увеличивается на указанное значение
    - Если товара нет в заказе, создается новая позиция
    - Проверяется наличие товара на складе (поле `quantity` в таблице `products`)
    - Если товара недостаточно, возвращается ошибка 400
    
    **Возвращает:**
    - Объект позиции заказа (OrderItem) с обновленными данными
    """,
)
def add_item_to_order(
    request: AddItemToOrderRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint для добавления товара в заказ.
    
    Проверяет наличие заказа и товара, а также достаточность товара на складе.
    Если товар уже есть в заказе - увеличивает его количество.
    """
    logger.info(
        f"Получен запрос на добавление товара: order_id={request.order_id}, "
        f"product_id={request.product_id}, quantity={request.quantity}"
    )
    
    try:
        result = OrderService.add_item_to_order(db, request)
        logger.info(
            f"Товар успешно добавлен в заказ: order_id={request.order_id}, "
            f"product_id={request.product_id}, order_item_id={result.id}"
        )
        return result
    except ValueError as e:
        error_message = str(e)
        if "не найден" in error_message:
            logger.warning(f"Ресурс не найден: {error_message}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_message
            )
        else:
            logger.warning(f"Ошибка валидации: {error_message}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
    except Exception as e:
        logger.error(f"Неожиданная ошибка при добавлении товара в заказ: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )
