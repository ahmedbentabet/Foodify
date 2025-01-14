from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
<<<<<<< HEAD
from models.base_model import BaseModel

=======
from models.base_model import BaseModel, Base
>>>>>>> origin/Ahmed_Branch

class Review(BaseModel, Base):
    """Review model"""
    
    __tablename__ = 'reviews'

<<<<<<< HEAD
    user_id = Column(String(36), ForeignKey('user.id'), nullable=False)
    restaurant_id = Column(String(36), ForeignKey('restaurant.id'),
                           nullable=False)
=======
    client_id = Column(String(60), ForeignKey('clients.id', ondelete="CASCADE"), nullable=False)
    restaurant_id = Column(String(60), ForeignKey('restaurants.id', name='rstau_ibfk_1', ondelete="CASCADE"), nullable=False)
>>>>>>> origin/Ahmed_Branch
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)

    client = relationship("Client", back_populates="reviews")
    restaurant = relationship("Restaurant", back_populates="reviews")

    def __init__(self, *args, **kwargs):
        """Initialize review"""
        super().__init__(*args, **kwargs)
