from datetime import datetime, UTC

from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, JSON, Boolean, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)


class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String)


# Справочники
class OrderStatus(Base):
    __tablename__ = "order_statuses"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False)


class OrderPriority(Base):
    __tablename__ = "order_priorities"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False)


class PaymentMethod(Base):
    __tablename__ = "payment_methods"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False)


class PaymentStatus(Base):
    __tablename__ = "payment_statuses"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False)


class DeliveryType(Base):
    __tablename__ = "delivery_types"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False)
    has_address = Column(Boolean, default=False)


class OrderSource(Base):
    __tablename__ = "order_sources"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False)


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("clients.id"))
    order_number = Column(String, unique=True, nullable=False)
    subtotal = Column(Numeric(10, 2), default=0)
    discount_amount = Column(Numeric(10, 2), default=0)
    tax_amount = Column(Numeric(10, 2), default=0)
    shipping_amount = Column(Numeric(10, 2), default=0)
    total_amount = Column(Numeric(10, 2), default=0)
    paid_amount = Column(Numeric(10, 2), default=0)
    delivery_address = Column(String)
    city = Column(String)
    zipcode = Column(String)
    recipient_name = Column(String)
    phone = Column(String)
    email = Column(String)
    tracking_number = Column(String)
    order_date = Column(DateTime, default=lambda: datetime.now(UTC))
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    
    # Внешние ключи справочников
    status_id = Column(Integer, ForeignKey("order_statuses.id"))
    priority_id = Column(Integer, ForeignKey("order_priorities.id"))
    payment_method_id = Column(Integer, ForeignKey("payment_methods.id"))
    payment_status_id = Column(Integer, ForeignKey("payment_statuses.id"))
    delivery_type_id = Column(Integer, ForeignKey("delivery_types.id"))
    source_id = Column(Integer, ForeignKey("order_sources.id"))
    
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    product_name = Column(String)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    discount_percent = Column(Integer, default=0)
    discount_amount = Column(Numeric(10, 2), default=0)
    total_price = Column(Numeric(10, 2), nullable=False)
    variant = Column(String)  # JSONB/String для характеристик
    
    order = relationship("Order", back_populates="items")
    product = relationship("Product")


class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    payment_method_id = Column(Integer, ForeignKey("payment_methods.id"))
    transaction_id = Column(String)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String)  # JSONB/String
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))


class OrderStatusHistory(Base):
    __tablename__ = "order_status_history"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("order_statuses.id"))
    changed_by = Column(String)
    notes = Column(String)
    changed_at = Column(DateTime, default=lambda: datetime.now(UTC))


class OrderComment(Base):
    __tablename__ = "order_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    author_name = Column(String)
    comment_text = Column(Text)
    is_internal = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
