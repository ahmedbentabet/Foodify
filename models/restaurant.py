from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from base_model import BaseModel, Base

class Restaurant(BaseModel, Base):
    """Restaurant model"""
    
    __tablename__ = 'restaurants'

    name = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)

    reviews = relationship("Review", back_populates="restaurant", cascade="all, delete-orphan")
    menu_items = relationship("MenuItem", back_populates="restaurant", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="restaurant", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """Initialize restaurant"""
        super().__init__(*args, **kwargs)

