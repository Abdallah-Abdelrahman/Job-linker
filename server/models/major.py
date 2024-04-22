"""Major Module"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.basemodel import Base, BaseModel


class Major(Base, BaseModel):
    """Major Class"""

    __tablename__ = "majors"

    name = Column(String(100), nullable=False)

    # Relationship with Jobs & Candidates
    jobs = relationship("Job", back_populates="major")
    candidates = relationship('Candidate', back_populates='major')

    def __repr__(self):
        """Return a string representation of the Major instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.name}"

    @property
    def to_dict(self):
        """Return a dictionary representation of the Major instance"""
        major_dict = super().to_dict
        major_dict["name"] = self.name
        return major_dict
