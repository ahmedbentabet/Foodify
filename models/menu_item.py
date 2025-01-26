from typing import Any, Optional
from sqlalchemy import Column, String, Boolean, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class MenuItem(BaseModel, Base):
    """
    MenuItem model representing items available for order.

    Attributes:
        restaurant_id: ID of the restaurant offering this item
        name: Name of the menu item
        price: Price of the item
        is_available: Whether the item is currently available
        image_url: Optional URL to item's image
    """

    __tablename__ = "menu_items"

    restaurant_id: str = Column(
        String(60),
        ForeignKey("restaurants.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: str = Column(String(100), nullable=False)
    price: float = Column(
        DECIMAL(10, 2), nullable=False
    )  # Using DECIMAL instead of Float for price
    is_available: bool = Column(Boolean, default=True)
    """ Path to image file """
    image_url: Optional[str] = Column(String(255), nullable=True)

    restaurant = relationship("Restaurant", back_populates="menu_items")
    order_items = relationship(
        "OrderItem", back_populates="menu_item", cascade="all, delete-orphan"
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize menu item"""
        super().__init__(*args, **kwargs)
