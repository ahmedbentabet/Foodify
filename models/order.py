from sqlalchemy import Column, Integer, DECIMAL, ForeignKey, Enum, String, DateTime
from sqlalchemy.orm import relationship
<<<<<<< HEAD
from models.base_model import BaseModel

=======
from models.base_model import BaseModel, Base
from models.client import Client
from datetime import datetime
>>>>>>> origin/Ahmed_Branch


<<<<<<< HEAD
    user_id = Column(String(36), ForeignKey('user.id'), nullable=False)
    restaurant_id = Column(String(36), ForeignKey('restaurant.id'),
                           nullable=False)
    # Store item list as a serialized string
    items = Column(String, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String, nullable=False)  # e.g., 'pending',
    # 'completed', 'cancelled'
    payment_details = Column(String, nullable=True)
=======
class Order(BaseModel, Base):
    """Order model"""
>>>>>>> origin/Ahmed_Branch

    __tablename__ = 'orders'

    client_id = Column(String(60), ForeignKey('clients.id', ondelete="CASCADE"),nullable=False)
    status = Column(String(20), nullable=False, default="active")  # active, completed, cancelled
    total_price = Column(DECIMAL(10, 2), nullable=False)  # Added total_price field
    order_date = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """Initialize order"""
        super().__init__(*args, **kwargs)