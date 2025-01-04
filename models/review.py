from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from base_model import BaseModel, Base

class Review(BaseModel, Base):
    """Review model"""
    
    __tablename__ = 'reviews'

    client_id = Column(String(60), ForeignKey('clients.id'), nullable=False)
    restaurant_id = Column(String(60), ForeignKey('restaurants.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)

    client = relationship("Client", back_populates="reviews")
    restaurant = relationship("Restaurant", back_populates="reviews")

    def __init__(self, *args, **kwargs):
        """Initialize review"""
        super().__init__(*args, **kwargs)
