"""UserFile model to keep track of the files each user has uploaded"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import backref, relationship

from server.models.base_model import Base, BaseModel


class UserFile(BaseModel, Base):
    """UserFile Model"""

    __tablename__ = "user_files"

    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    file_url = Column(String(200), nullable=False)
    original_filename = Column(String(200), nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)

    # Relationship with User
    user = relationship(
        "User", backref=backref("user_files", cascade="all, delete-orphan")
    )

    def __repr__(self):
        """Return a string representation of the UserFile instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.file_url}"
