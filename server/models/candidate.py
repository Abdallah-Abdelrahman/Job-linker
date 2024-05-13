"""Candidate Class"""

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import backref, relationship

from server.models.base_model import Base, BaseModel
from server.models.language import candidate_languages
from server.models.skill import candidate_skills


class Candidate(BaseModel, Base):
    """Candidate Model"""

    __tablename__ = "candidates"

    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    major_id = Column(String(60), ForeignKey("majors.id"), nullable=False)

    # Relationship with User & skills
    user = relationship('User',
                        backref='candidate',
                        single_parent=True,
                        uselist=False,
                        cascade='all, delete-orphan')
    skills = relationship(
            "Skill",
            secondary=candidate_skills,
            back_populates="candidates",
            cascade="all, delete"
            )

    # Relationship with Languages and associative table
    languages = relationship(
        "Language",
        secondary=candidate_languages,
        back_populates="candidates",
    )

    # Relationship with Application
    applications = relationship(
        "Application",
        backref="candidate",
        cascade="all, delete-orphan"
    )

    experiences = relationship('WorkExperience',
                               backref='candidate',
                               cascade='all, delete-orphan')

    def __repr__(self):
        """Return a string representation of the Candidate instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.major.name}"

    @property
    def to_dict(self):
        """Return a dictionary representation of the Candidate instance"""
        candidate_dict = super().to_dict
        candidate_dict["name"] = self.user.name
        candidate_dict["email"] = self.user.email
        candidate_dict["bio"] = self.user.bio
        candidate_dict["major"] = self.major.name
        candidate_dict["skills"] = [skill.name for skill in self.skills]
        candidate_dict["experiences"] = [
            {
                "title": xp.title,
                "start_date": xp.start_date,
                "end_date": xp.end_date,
                "location": xp.location,
                "description": xp.description,
            }
            for xp in self.experiences
        ]
        candidate_dict["languages"] = [lang.name for lang in self.languages]
        candidate_dict.pop("user", None)
        return candidate_dict
