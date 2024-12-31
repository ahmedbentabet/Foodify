from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel

class Review(BaseModel):
    """Review model"""
    
    __tablename__ = 'reviews'

    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)

    client = relationship("Client", back_populates="reviews")
    restaurant = relationship("Restaurant", back_populates="reviews")

    def __init__(self, *args, **kwargs):
        """Initialize review"""
        super().__init__(*args, **kwargs)
