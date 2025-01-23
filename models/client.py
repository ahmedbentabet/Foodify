#!/usr/bin/env python3
"""Client model module defining the Client class."""
from typing import Optional, Any
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from flask_login import UserMixin


class Client(BaseModel, Base, UserMixin):
    """
    Client model representing application users.

    Attributes:
        username: Client's username
        address: Client's address
        email: Client's email address
        password: Hashed password
        latitude: Geographic latitude
        longitude: Geographic longitude
        phone: Contact phone number
        delivery_instructions: Special delivery instructions
    """

    __tablename__ = "clients"

    username: str = Column(String(70), nullable=False)
    address: str = Column(String(70), nullable=False)
    email: str = Column(String(100), unique=True, nullable=False)
    password: str = Column(String(128), nullable=False)
    latitude: Optional[float] = Column(Float, nullable=True)
    longitude: Optional[float] = Column(Float, nullable=True)
    phone: Optional[str] = Column(String(20), nullable=True)
    delivery_instructions: Optional[str] = Column(String(500), nullable=True)

    reviews = relationship(
        "Review", back_populates="client", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="client",
                          cascade="all, delete-orphan")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize a new Client instance."""
        super().__init__(*args, **kwargs)

    def update(self, **kwargs: Any) -> None:
        """
        Update client attributes.

        Args:
            **kwargs: Arbitrary keyword arguments for
                                updating client attributes
        """
        allowed_fields = ["email", "address"]
        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(self, key, value)
        self.save()
