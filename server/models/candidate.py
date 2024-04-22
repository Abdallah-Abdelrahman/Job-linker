"""Candidate Class"""

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models.basemodel import Base, BaseModel
from models.skill import candidate_skills


class Candidate(Base, BaseModel):
    """Candidate Model"""

    __tablename__ = "candidates"

    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    major = Column(String(100), nullable=False)
    skills = Column(String(500))

    # Relationship with User & skills
    user = relationship("User", back_populates="candidate")
    skills = relationship(
        "Skill",
        secondary=candidate_skills,
        back_populates="candidates",
    )

    def __repr__(self):
        """Return a string representation of the Candidate instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.major}"

    @property
    def to_dict(self):
        """Return a dictionary representation of the Candidate instance"""
        candidate_dict = super().to_dict
        candidate_dict["major"] = self.major
        candidate_dict["skills"] = self.skills
        return candidate_dict
