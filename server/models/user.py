"""User Class"""

from flask_login import UserMixin
from sqlalchemy import JSON, TEXT, Boolean, Column, Enum, String
from sqlalchemy.orm import backref, relationship

from server.models.base_model import Base, BaseModel


class User(BaseModel, Base, UserMixin):
    """User Model"""

    __tablename__ = "users"

    name = Column(String(128), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(Enum("candidate", "recruiter"), nullable=False)
    contact_info = Column(JSON)
    bio = Column(TEXT)
    image_url = Column(String(200))
    verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    profile_complete = Column(Boolean, default=False)

    def __repr__(self):
        """Return a string representation of the User instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.email}"
