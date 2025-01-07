#!/usr/bin/python3
"""This module defines a class to manage db storage for Foodify"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base, BaseModel
from models.client import Client
from models.menu_item import MenuItem
from models.order_item import OrderItem
from models.order import Order
from models.restaurant import Restaurant
from models.review import Review

from typing import Dict, Any, Optional, List


classes = [Client, Restaurant, MenuItem, Review, Order, OrderItem]


class DBStorage:
    """Database Storage Class"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize database connection"""
        self.environment = getenv("FOOD_ENV", "development")
        user = getenv("FOOD_MYSQL_USER", "root")
        pwd = getenv("FOOD_MYSQL_PWD", "root")
        host = getenv("FOOD_MYSQL_HOST", "127.0.0.1")
        db = getenv("FOOD_MYSQL_DB", "foodify_db")

        self.__engine = create_engine(
            f"mysql+mysqldb://{user}:{pwd}@{host}/{db}", pool_pre_ping=True
        )

    def reload(self) -> None:
        """Create tables and session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def new(self, obj: BaseModel) -> None:
        """Add object to current database session"""
        if obj:
            self.__session.add(obj)

    def save(self) -> None:
        """Commit changes to database"""
        try:
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise e

    def delete(self, obj: Optional[BaseModel] = None) -> None:
        """Delete object from current database session"""
        if obj:
            self.__session.delete(obj)

    def get(self, cls: Any, id: str) -> Optional[BaseModel]:
        """Retrieve object by class and id"""
        if cls and id:
            return self.__session.query(cls).filter(cls.id == id).first()
        return None

    def all(
        self, cls: Optional[Any] = None, page: int = -1, per_page: int = -1
    ) -> Dict[str, BaseModel]:
        """Query all objects of given class with pagination"""
        objects = {}

        if cls is None:
            # Query all types of objects
            for model_class in classes:
                for obj in self.__session.query(model_class).all():
                    key = f"{model_class.__name__}.{obj.id}"
                    objects[key] = obj
        else:
            if page < 0 and per_page < 0:
                # Query only objects of the specified class
                for obj in self.__session.query(cls).all():
                    key = f"{cls.__name__}.{obj.id}"
                    objects[key] = obj
            else:
                # Query with pagination
                query = self.__session.query(cls)
                total = query.count()
                offset = (page - 1) * per_page
                items = query.offset(offset).limit(per_page).all()

                for obj in items:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    objects[key] = obj

                return {
                    "items": objects,
                    "page": page,
                    "per_page": per_page,
                    "total": total,
                }

        return objects

    def search(
        self, cls: Any, filters: Dict[str, Any],
        nested_filters: Dict[str, Dict] = None
    ) -> List[BaseModel]:
        """
        Enhanced search method with nested relationship filtering

        Example:
        filters = {"name": "Pizza Hut"}
        nested_filters = {"menu_items": {"name": "juice"}}
        """
        query = self.__session.query(cls)

        # Apply main filters
        for key, value in filters.items():
            if hasattr(cls, key):
                query = query.filter(getattr(cls, key).ilike(f"%{value}%"))

        # Apply nested filters
        if nested_filters:
            for relation, rel_filters in nested_filters.items():
                if hasattr(cls, relation):
                    for key, value in rel_filters.items():
                        query = query.filter(
                            getattr(cls, relation).any(**{key: value})
                            )

        return query.all()

    def close(self) -> None:
        """Close current session"""
        self.__session.close()

    def count(self, cls: Optional[Any] = None) -> int:
        """Count number of objects in storage"""
        if cls:
            return self.__session.query(cls).count()
        return 0
