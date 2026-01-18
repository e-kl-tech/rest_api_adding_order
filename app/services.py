from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from decimal import Decimal
import logging
from app.models import Order, OrderItem, Product
from app.schemas import AddItemToOrderRequest, OrderItemResponse

logger = logging.getLogger(__name__)


class OrderService:
    @staticmethod
    def add_item_to_order(db: Session, request: AddItemToOrderRequest) -> OrderItemResponse:
        """
        Добавляет товар в заказ. Если товар уже есть - увеличивает количество.
        Проверяет наличие товара на складе.
        """
        logger.info(f"Добавление товара в заказ: order_id={request.order_id}, product_id={request.product_id}, quantity={request.quantity}")
        
        # Проверяем существование заказа
        order = db.query(Order).filter(Order.id == request.order_id).first()
        if not order:
            logger.warning(f"Заказ с ID {request.order_id} не найден")
            raise ValueError(f"Заказ с ID {request.order_id} не найден")
        
        logger.debug(f"Заказ найден: order_number={order.order_number}")
        
        # Проверяем существование товара и его количество на складе
        product = db.query(Product).filter(Product.id == request.product_id).first()
        if not product:
            logger.warning(f"Товар с ID {request.product_id} не найден")
            raise ValueError(f"Товар с ID {request.product_id} не найден")
        
        logger.debug(f"Товар найден: name={product.name}, quantity_available={product.quantity}, price={product.price}")
        
        # Проверяем наличие товара на складе
        current_quantity_in_order = 0
        existing_item = db.query(OrderItem).filter(
            OrderItem.order_id == request.order_id,
            OrderItem.product_id == request.product_id
        ).first()
        
        if existing_item:
            current_quantity_in_order = existing_item.quantity
            logger.debug(f"Товар уже есть в заказе: текущее количество={current_quantity_in_order}")
        
        required_quantity = current_quantity_in_order + request.quantity
        
        if product.quantity < required_quantity:
            logger.warning(
                f"Недостаточно товара на складе: product_id={request.product_id}, "
                f"доступно={product.quantity}, требуется={required_quantity}"
            )
            raise ValueError(
                f"Недостаточно товара на складе. "
                f"Доступно: {product.quantity}, требуется: {required_quantity}"
            )
        
        # Если товар уже есть в заказе - увеличиваем количество
        if existing_item:
            old_quantity = existing_item.quantity
            existing_item.quantity += request.quantity
            existing_item.total_price = Decimal(existing_item.quantity) * existing_item.unit_price
            db.commit()
            db.refresh(existing_item)
            logger.info(
                f"Количество товара увеличено: order_id={request.order_id}, "
                f"product_id={request.product_id}, было={old_quantity}, стало={existing_item.quantity}"
            )
            return OrderItemResponse.model_validate(existing_item)
        
        # Создаем новую позицию в заказе
        unit_price = Decimal(str(product.price))
        new_item = OrderItem(
            order_id=request.order_id,
            product_id=request.product_id,
            product_name=product.name,
            quantity=request.quantity,
            unit_price=unit_price,
            total_price=unit_price * request.quantity
        )
        
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        
        logger.info(
            f"Новая позиция создана: order_id={request.order_id}, "
            f"product_id={request.product_id}, quantity={request.quantity}, "
            f"total_price={new_item.total_price}"
        )
        
        return OrderItemResponse.model_validate(new_item)
