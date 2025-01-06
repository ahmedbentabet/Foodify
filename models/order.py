from sqlalchemy import Column, Integer, DECIMAL, ForeignKey, Enum, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Order(BaseModel, Base):
    """Order model"""

    __tablename__ = 'orders'

    client_id = Column(String(60), ForeignKey('clients.id', ondelete="CASCADE"),nullable=False)
    restaurant_id = Column(String(60), ForeignKey('restaurants.id', ondelete="CASCADE"),nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum('pending', 'completed', name='order_status'), default='pending')

    client = relationship("Client", back_populates="orders")
    restaurant = relationship("Restaurant", back_populates="orders")

    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """Initialize order"""
        super().__init__(*args, **kwargs)