#!/usr/bin/env python3
"""Client model module"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from base_model import BaseModel, Base

class Client(BaseModel, Base):
    """Client model"""
    
    __tablename__ = 'clients'

    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    address = Column(String(500), nullable=False)  # Combined address field

    reviews = relationship("Review", back_populates="client", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="client", cascade="all, delete-orphan")


    def __init__(self, *args, **kwargs):
        """Initialize client"""
        super().__init__(*args, **kwargs)

