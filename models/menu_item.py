from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel

class MenuItem(BaseModel):
    """MenuItem model"""
    
    __tablename__ = 'menu_items'

    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    is_available = Column(Boolean, default=True)

    restaurant = relationship("Restaurant", back_populates="menu_items")
    order_items = relationship("OrderItem", back_populates="menu_item")

    def __init__(self, *args, **kwargs):
        """Initialize menu item"""
        super().__init__(*args, **kwargs)
