#!/usr/bin/python3
"""
Database storage module for Foodify application.

This module provides the DBStorage class that handles all database operations
including CRUD operations, session management, and connection handling.
"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy.engine import Engine
from models.base_model import Base, BaseModel
from models.client import Client
from models.menu_item import MenuItem
from models.order_item import OrderItem
from models.order import Order
from models.restaurant import Restaurant
from models.review import Review

from typing import Dict, Any, Optional, List, Type, Union
from contextlib import contextmanager


ModelType = Type[Union[Client, Restaurant, MenuItem, Review, Order, OrderItem]]
CLASSES: List[ModelType] = [Client, Restaurant, MenuItem, Review, Order,
                            OrderItem]


class DBStorage:
    """
    Database Storage Class for managing database operations.

    Attributes:
        __engine: SQLAlchemy engine instance
        __session: SQLAlchemy session instance
    """

    __engine: Optional[Engine] = None
    __session: Optional[scoped_session] = None

    def __init__(self) -> None:
        """
        Initialize database connection with optimized settings.

        Environment variables:
            FOOD_MYSQL_USER: Database username
            FOOD_MYSQL_PWD: Database password
            FOOD_MYSQL_HOST: Database host
            FOOD_MYSQL_DB: Database name
        """
        user = getenv("FOOD_MYSQL_USER", "root")
        pwd = getenv("FOOD_MYSQL_PWD", "root")
        host = getenv("FOOD_MYSQL_HOST", "127.0.0.1")
        db = getenv("FOOD_MYSQL_DB", "foodify_db")

        self.__engine = create_engine(
            f"mysql+mysqldb://{user}:{pwd}@{host}/{db}",
            pool_pre_ping=True,  # Check connection before using
            pool_recycle=300,  # Recycle connections every 5 minutes
            pool_size=5,  # Smaller pool size
            max_overflow=10,  # Allow more temp connections if needed
            pool_timeout=30,  # Connection timeout
            connect_args={"connect_timeout": 60, "read_timeout": 30},
        )
        self.__session = None

    def reload(self) -> None:
        """
        Create database tables and initialize session.

        Raises:
            Exception: If database connection or table creation fails
        """
        try:
            Base.metadata.create_all(self.__engine)
            session_factory = sessionmaker(
                bind=self.__engine,
                expire_on_commit=False,
                autoflush=True
            )
            Session = scoped_session(session_factory)
            self.__session = Session
        except Exception as e:
            print(f"Database reload error: {str(e)}")
            if self.__session:
                self.__session.remove()
            raise

    def new(self, obj: BaseModel) -> None:
        """
        Add new object to current database session.

        Args:
            obj: BaseModel instance to add
        """
        if obj and self.__session:
            self.__session.add(obj)

    def save(self) -> None:
        """
        Commit current session changes to database.

        Raises:
            Exception: If commit fails
        """
        if not self.__session:
            return

        try:
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise RuntimeError(f"Save operation failed: {str(e)}") from e

    def delete(self, obj: Optional[BaseModel] = None) -> None:
        """Delete object from current database session"""
        if obj:
            try:
                self.__session.delete(obj)
                self.__session.flush()  # Added flush() call
            except Exception as e:
                self.__session.rollback()
                print(f"Error deleting object: {e}")  # Added error logging

    def get(self, cls: Any, id: str) -> Optional[BaseModel]:
        """Retrieve object by class and id"""
        if cls and id:
            return self.__session.query(cls).filter(cls.id == id).first()
        return None

    def all(self, cls=None) -> Dict[str, BaseModel]:
        """Query objects"""
        try:
            if cls:
                objects = self.__session.query(cls).all()
            else:
                objects = []
                for c in CLASSES:
                    objects.extend(self.__session.query(c).all())

            return {
                f"{obj.__class__.__name__}.{obj.id}": obj for obj in objects
            }

        except Exception as e:
            self.__session.rollback()
            raise e

    def search(
        self,
        cls: ModelType,
        filters: Dict[str, Any],
        nested_filters: Optional[Dict[str, Dict[str, Any]]] = None
    ) -> List[BaseModel]:
        """
        Enhanced search method supporting nested relationship filtering.

        Args:
            cls: Model class to search
            filters: Primary filter conditions
            nested_filters: Filters for related models

        Returns:
            List of matching model instances

        Example:
            filters = {"name": "Pizza Hut"}
            nested_filters = {"menu_items": {"name": "juice"}}
        """
        if not self.__session:
            return []

        query = self.__session.query(cls)

        # Apply main filters with type checking
        for key, value in filters.items():
            if hasattr(cls, key):
                query = query.filter(getattr(cls, key).ilike(f"%{value}%"))

        # Apply nested relationship filters
        if nested_filters:
            for relation, rel_filters in nested_filters.items():
                if hasattr(cls, relation):
                    for key, value in rel_filters.items():
                        query = query.filter(
                            getattr(cls, relation).any(**{key: value})
                        )

        return query.all()

    def close(self) -> None:
        """Close session safely"""
        if self.__session:
            try:
                self.__session.remove()  # Safe to call on scoped_session
            except Exception as e:
                print(f"Error closing session: {e}")
                pass

    def count(self, cls: Optional[Any] = None) -> int:
        """Count number of objects in storage"""
        if cls:
            return self.__session.query(cls).count()
        return 0

    def rollback(self) -> None:
        """Rollback current database session"""
        try:
            if self.__session:
                self.__session.rollback()
        except Exception as e:
            print(f"Error during rollback: {e}")

    @contextmanager
    def session_scope(self) -> Session:
        """
        Provide a transactional scope around operations.

        Yields:
            Active database session

        Raises:
            Exception: If session operations fail
        """
        session = self.refresh_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            if session:
                session.rollback()
            raise RuntimeError(f"Session operation failed: {str(e)}") from e
        finally:
            if session:
                session.remove()

    def refresh_session(self):
        """Create a fresh session"""
        try:
            if self.__session:
                self.__session.close()

            # Create session factory
            session_factory = sessionmaker(
                bind=self.__engine, expire_on_commit=False, autoflush=True
            )
            # Create scoped session
            Session = scoped_session(session_factory)
            self.__session = Session
            return self.__session
        except Exception as e:
            print(f"Error refreshing session: {e}")
            raise
