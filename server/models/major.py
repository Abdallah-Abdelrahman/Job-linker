"""Major Module"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from server.models.base_model import Base, BaseModel


class Major(BaseModel, Base):
    """Major Class"""

    __tablename__ = "majors"

    name = Column(String(100), nullable=False, unique=True)

    # Relationship with Jobs & Candidates
    jobs = relationship("Job",
                        backref="major",
                        cascade="all, delete-orphan"
                        )
    candidates = relationship("Candidate",
                              backref="major",
                              cascade="all, delete-orphan")

    def __repr__(self):
        """Return a string representation of the Major instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.name}"
