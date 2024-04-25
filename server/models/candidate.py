"""Candidate Class"""

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from server.models.base_model import Base, BaseModel
from server.models.skill import candidate_skills


class Candidate(Base, BaseModel):
    """Candidate Model"""

    __tablename__ = "candidates"

    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    major_id = Column(String(60), ForeignKey("majors.id"), nullable=False)

    # Relationship with User & skills
    user = relationship("User", backref="candidate")
    skills = relationship(
        "Skill",
        secondary=candidate_skills,
        back_populates="candidates",
    )
    # Relationship with Major
    major = relationship("Major", back_populates="candidates")

    def __repr__(self):
        """Return a string representation of the Candidate instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.major.name}"

    @property
    def to_dict(self):
        """Return a dictionary representation of the Candidate instance"""
        candidate_dict = super().to_dict
        candidate_dict["major"] = self.major.name
        candidate_dict["skills"] = [skill.name for skill in self.skills]
        candidate_dict["experiences"] = [e.title for e in self.experiences
                                         if hasattr(self, "experiences")]
        return candidate_dict
