from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from base_model import BaseModel, Base

class OrderItem(BaseModel, Base):
    """OrderItem model"""
    
    __tablename__ = 'order_items'

    order_id = Column(String(60), ForeignKey('orders.id'), nullable=False)
    menu_item_id = Column(String(60), ForeignKey('menu_items.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="order_items")
    menu_item = relationship("MenuItem", back_populates="order_items")

    def __init__(self, *args, **kwargs):
        """Initialize order item"""
        super().__init__(*args, **kwargs)
