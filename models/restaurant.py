from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from base_model import BaseModel

class Restaurant(BaseModel):
    """
    Restaurant model to store restaurant information.
    """
    __tablename__ = 'restaurant'

    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    owner_id = Column(String(36), ForeignKey('user.id'), nullable=False)
    cuisine_type = Column(String, nullable=True)

    # Relationship to the User who owns the restaurant
    owner = relationship('User', backref='restaurants')
