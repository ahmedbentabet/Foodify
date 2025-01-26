"""Restaurant model module defining Restaurant class."""
from typing import Optional
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Restaurant(BaseModel, Base):
    """
    Restaurant model representing food establishments.

    Attributes:
        name: Restaurant name
        city: Restaurant location
        logo_url: URL to restaurant logo
    """

    __tablename__ = "restaurants"

    name: str = Column(String(100), nullable=False)
    city: str = Column(String(100), nullable=False)
    logo_url: Optional[str] = Column(
        String(255), nullable=True
    )  # URL or path to restaurant icon

    reviews = relationship(
        "Review",
        back_populates="restaurant",
        cascade="all, delete, save-update",
    )
    menu_items = relationship(
        "MenuItem", back_populates="restaurant", cascade="all, delete-orphan"
    )

    def __init__(self, *args, **kwargs):
        """Initialize restaurant"""
        super().__init__(*args, **kwargs)
