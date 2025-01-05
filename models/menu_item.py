from sqlalchemy import Column, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel


class MenuItem(BaseModel):
    """
    Menu Item model to store restaurant menu items.
    """
    __tablename__ = 'menu_item'

    name = Column(String, nullable=False)
    item_type = Column(String, nullable=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    availability = Column(Boolean, default=True)
    restaurant_id = Column(String(36), ForeignKey('restaurant.id'),
                           nullable=False)
    order_id = Column(String(36), ForeignKey('order.id'), nullable=True)

    # Relationships
    restaurant = relationship('Restaurant', backref='menu_items')
    order = relationship('Order', backref='ordered_items')
