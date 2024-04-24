"""User Class"""

from sqlalchemy import Column, Enum, String

from server.models.base_model import Base, BaseModel


class User(Base, BaseModel):
    """User Model"""

    __tablename__ = "users"

    name = Column(String(128), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(Enum("candidate", "recruiter"), nullable=False)
    contact_info = Column(String(100))
    bio = Column(String(500))
    image_url = Column(String(200))

    def __repr__(self):
        """Return a string representation of the User instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.email}"
