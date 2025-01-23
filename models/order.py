from typing import Any
from datetime import datetime
from sqlalchemy import Column, DECIMAL, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Order(BaseModel, Base):
    """
    Order model representing customer purchases.

    Attributes:
        client_id: ID of the client making the order
        status: Current order status (active/completed/cancelled)
        total_price: Total cost of the order
        order_date: Timestamp when order was placed
    """

    __tablename__ = "orders"

    client_id: str = Column(String(60), ForeignKey("clients.id",
                                                   ondelete="CASCADE"),
                            nullable=False)
    status: str = Column(String(20), nullable=False, default="active")
    total_price: float = Column(DECIMAL(10, 2), nullable=False)
    order_date: datetime = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize order"""
        super().__init__(*args, **kwargs)
