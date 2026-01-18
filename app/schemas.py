from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class AddItemToOrderRequest(BaseModel):
    order_id: int = Field(..., description="ID заказа", gt=0)
    product_id: int = Field(..., description="ID номенклатуры", gt=0)
    quantity: int = Field(..., gt=0, description="Количество товара")
    
    class Config:
        json_schema_extra = {
            "example": {
                "order_id": 1,
                "product_id": 5,
                "quantity": 3
            }
        }


class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    product_name: Optional[str]
    quantity: int
    unit_price: Decimal
    total_price: Decimal
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "order_id": 1,
                "product_id": 5,
                "product_name": "Товар",
                "quantity": 3,
                "unit_price": "1000.00",
                "total_price": "3000.00"
            }
        }


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Недостаточно товара на складе",
                "detail": "Доступно: 5, требуется: 10"
            }
        }
