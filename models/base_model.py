#!/usr/bin/env python3
"""Base model module providing common functionality for all models."""
from typing import Any, Dict
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """
    Base class for all Foodify models providing common functionality.

    Attributes:
        id: Unique identifier for each instance
        created_at: Timestamp of instance creation
        updated_at: Timestamp of last update
    """

    __abstract__ = True

    id: str = Column(String(60), primary_key=True, nullable=False)
    created_at: datetime = Column(
        DateTime, default=datetime.utcnow, nullable=False)
    updated_at: datetime = Column(
        DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize a new BaseModel instance.

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        super().__init__()  # Call parent class constructor
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.now()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.now()

    def __str__(self) -> str:
        """
        Return string representation of the instance.

        Returns:
            String representation of the model instance
        """
        cls = (str(type(self)).split(".")[-1]).split("'")[0]
        return "[{}] ({}) {}".format(cls, self.id, self.__dict__)

    def save(self) -> None:
        """Update the updated_at timestamp and save instance to storage."""
        self.updated_at = datetime.now()
        import models

        models.storage.new(self)
        models.storage.save()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert instance to dictionary format.

        Returns:
            Dictionary representation of the model instance
        """
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update(
            {"__class__": (str(type(self)).split(".")[-1]).split("'")[0]}
        )
        dictionary["created_at"] = self.created_at.isoformat()
        dictionary["updated_at"] = self.updated_at.isoformat()
        if "_sa_instance_state" in dictionary:
            del dictionary["_sa_instance_state"]
        return dictionary

    def delete(self) -> None:
        """Delete the current instance from storage."""
        import models

        models.storage.delete(self)
