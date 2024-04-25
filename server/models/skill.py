"""Skills Model"""
from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import relationship

from server.models.base_model import BaseModel, Base

# Association table for Candidate-Skill many-to-many relationship
candidate_skills = Table(
    "candidate_skills",
    Base.metadata,
    Column("candidate_id", String(60), ForeignKey("candidates.user_id")),
    Column("skill_id", String(60), ForeignKey("skills.id")),
)

# Association table for Job-Skill many-to-many relationship
job_skills = Table(
    "job_skills",
    Base.metadata,
    Column("job_id", String(60), ForeignKey("jobs.id")),
    Column("skill_id", String(60), ForeignKey("skills.id")),
)


class Skill(BaseModel, Base):
    """Skills Class"""

    __tablename__ = "skills"

    name = Column(String(100), nullable=False, unique=True, index=True)

    # Relationship with Candidate
    candidates = relationship(
        "Candidate",
        secondary=candidate_skills,
        back_populates="skills",
    )

    # Relationship with Job
    jobs = relationship(
        "Job",
        secondary=job_skills,
        back_populates="skills",
    )

    def __repr__(self):
        """Return a string representation of the Skill instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.name}"
