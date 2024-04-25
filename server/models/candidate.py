"""Candidate Class"""

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base
from models.skill import candidate_skills
from models.language import candidate_languages


class Candidate(BaseModel, Base):
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

    # Relationship with Languages and associative table
    languages = relationship(
            "Language",
            secondary=candidate_languages,
            back_populates="candidates")

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
        candidate_dict["experiences"] = [
                {
                    "title": xp.title,
                    "start_date": xp.start_date,
                    "end_date": xp.end_date,
                    "location": xp.location
                } for xp in self.experiences
        ]
        candidate_dict["languages"] = [lang.name for lang in self.languages]
        return candidate_dict
