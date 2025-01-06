from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

class Restaurant(BaseModel, Base):
    """Restaurant model"""
    
    __tablename__ = 'restaurants'

    name = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    logo_url = Column(String(255), nullable=True)  # URL or path to restaurant icon

    reviews = relationship("Review", back_populates="restaurant", cascade="all, delete, save-update")
    menu_items = relationship("MenuItem", back_populates="restaurant", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="restaurant", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """Initialize restaurant"""
        super().__init__(*args, **kwargs)
