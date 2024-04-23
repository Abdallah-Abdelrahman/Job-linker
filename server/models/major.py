"""Major Module"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel


class Major(Base, BaseModel):
    """Major Class"""

    __tablename__ = "majors"

    name = Column(String(100), nullable=False)

    # Relationship with Jobs & Candidates
    jobs = relationship("Job", back_populates="major")
    candidates = relationship("Candidate", back_populates="major")

    def __repr__(self):
        """Return a string representation of the Major instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.name}"
