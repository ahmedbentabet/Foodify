from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from base_model import BaseModel

class Review(BaseModel):
    """
    Review model to store user reviews for restaurants.
    """
    __tablename__ = 'review'

    user_id = Column(String(36), ForeignKey('user.id'), nullable=False)
    restaurant_id = Column(String(36), ForeignKey('restaurant.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)

    # Relationships
    user = relationship('User', backref='reviews')
    restaurant = relationship('Restaurant', backref='reviews')
