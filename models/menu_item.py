from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, ForeignKey
from sqlalchemy.orm import relationship
<<<<<<< HEAD
from models.base_model import BaseModel

=======
from models.base_model import BaseModel, Base
>>>>>>> origin/Ahmed_Branch

class MenuItem(BaseModel, Base):
    """MenuItem model"""
    
    __tablename__ = 'menu_items'

<<<<<<< HEAD
    name = Column(String, nullable=False)
    item_type = Column(String, nullable=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    availability = Column(Boolean, default=True)
    restaurant_id = Column(String(36), ForeignKey('restaurant.id'),
                           nullable=False)
    order_id = Column(String(36), ForeignKey('order.id'), nullable=True)
=======
    restaurant_id = Column(String(60), ForeignKey('restaurants.id', ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    is_available = Column(Boolean, default=True)
    image_url = Column(String(255), nullable=True)  # path to menu item image
>>>>>>> origin/Ahmed_Branch

    restaurant = relationship("Restaurant", back_populates="menu_items")
    order_items = relationship("OrderItem", back_populates="menu_item", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """Initialize menu item"""
        super().__init__(*args, **kwargs)
