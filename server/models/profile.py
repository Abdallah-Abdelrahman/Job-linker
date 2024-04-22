"""Profile Model"""

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from basemodel import Base, BaseModel


class Profile(Base, BaseModel):
    """Profile Model for the App"""

    __tablename__ = "profiles"

    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    contact_info = Column(String(100))
    bio = Column(String(500))
    image_url = Column(String(200))

    # Relationship with User
    user = relationship("User", back_populates="profile")

    def __init__(self, *args, **kwargs):
        """Initialize the Profile instance"""
        super().__init__(*args, **kwargs)

    def __repr__(self):
        """Return a string representation of the Profile instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.name}"

    @property
    def to_dict(self):
        """Return a dictionary representation of the Profile instance"""
        profile_dict = super().to_dict
        profile_dict["name"] = self.name
        profile_dict["contact_info"] = self.contact_info
        profile_dict["bio"] = self.bio
        profile_dict["image_url"] = self.image_url
        return profile_dict
