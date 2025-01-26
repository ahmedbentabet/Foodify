from typing import Any
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class OrderItem(BaseModel, Base):
    """
    OrderItem model representing individual items in an order.

    Attributes:
        order_id: ID of the parent order
        menu_item_id: ID of the menu item ordered
        quantity: Number of items ordered
    """

    __tablename__ = "order_items"

    order_id: str = Column(
        String(60),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
    )
    menu_item_id: str = Column(
        String(60),
        ForeignKey("menu_items.id", ondelete="CASCADE"),
        nullable=False,
    )
    quantity: int = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="order_items")
    menu_item = relationship("MenuItem", back_populates="order_items")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize order item"""
        super().__init__(*args, **kwargs)
