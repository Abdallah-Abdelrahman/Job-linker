"""Skills Model"""
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from models.basemodel import Base, BaseModel

# Association table for Candidate-Skill many-to-many relationship
candidate_skills = Table(
    "candidate_skills",
    Base.metadata,
    Column("candidate_id", String(60), ForeignKey("candidates.user_id")),
    Column("skill_id", Integer, ForeignKey("skills.id")),
)


class Skill(Base, BaseModel):
    """Skills Class"""

    __tablename__ = "skills"

    name = Column(String(100), nullable=False)

    # Relationship with Candidate
    candidates = relationship(
        "Candidate",
        secondary=candidate_skills,
        back_populates="skills",
    )

    def __repr__(self):
        """Return a string representation of the Skill instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.name}"

    @property
    def to_dict(self):
        """Return a dictionary representation of the Skill instance"""
        skill_dict = super().to_dict
        skill_dict["name"] = self.name
        return skill_dict
