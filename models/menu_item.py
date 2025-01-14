from sqlalchemy import Column, String, Boolean, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class MenuItem(BaseModel, Base):
    """MenuItem model"""

    __tablename__ = "menu_items"

    restaurant_id = Column(
        String(60), ForeignKey("restaurants.id", ondelete="CASCADE"),
        nullable=False
    )
    name = Column(String(100), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)  # Using DECIMAL instead of Float for price
    is_available = Column(Boolean, default=True)
    image_url = Column(String(255), nullable=True)  # path to menu item image

    restaurant = relationship("Restaurant", back_populates="menu_items")
    order_items = relationship(
        "OrderItem", back_populates="menu_item", cascade="all, delete-orphan"
    )

    def __init__(self, *args, **kwargs):
        """Initialize menu item"""
        super().__init__(*args, **kwargs)
