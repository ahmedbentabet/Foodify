from typing import Any, Optional
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Review(BaseModel, Base):
    """
    Review model for restaurant ratings and comments.

    Attributes:
        client_id: ID of the client who made the review
        restaurant_id: ID of the restaurant being reviewed
        rating: Numerical rating score
        comment: Optional text review
    """

    __tablename__ = "reviews"

    client_id: str = Column(String(60), ForeignKey("clients.id",
                                                   ondelete="CASCADE"),
                            nullable=False)
    restaurant_id: str = Column(String(60), ForeignKey("restaurants.id",
                                                       name="rstau_ibfk_1",
                                                       ondelete="CASCADE"),
                                nullable=False)
    rating: int = Column(Integer, nullable=False)
    comment: Optional[str] = Column(Text, nullable=True)

    client = relationship("Client", back_populates="reviews")
    restaurant = relationship("Restaurant", back_populates="reviews")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize review"""
        super().__init__(*args, **kwargs)
