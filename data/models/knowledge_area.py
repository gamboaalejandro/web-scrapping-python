import uuid

from sqlalchemy import Column,ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from data.models.university_institute import university_knowledge_association
from data.models.database import Base

"""
Class for knowledge areas data 
"""


class KnowledgeAreas(Base):
    #better name for tablename
    __tablename__ = 'knowledge_area'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(Text, nullable=False, unique=True)
    description = Column(Text, nullable=False)

    knowledge = relationship("SkillsForKnowledgeAreas", back_populates="knowledge_area")
    academic_program = relationship("AcademicPrograms", back_populates="knowledge_area")

    universities = relationship(
        'UniversityInstitute',
        secondary=university_knowledge_association,
        back_populates='knowledge_areas'
    )


class SkillsForKnowledgeAreas(Base):
    #better name for tablename
    __tablename__ = 'skills_for_knowledge_area'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(Text, nullable=False)

    knowledge_area_id = Column(UUID(as_uuid=True), ForeignKey('knowledge_area.id'))

    knowledge_area = relationship("KnowledgeAreas", back_populates="knowledge")


class AcademicPrograms(Base):
    #better name for tablename
    __tablename__ = 'academic_program'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    KnowledgeAreas_id = Column(UUID(as_uuid=True), ForeignKey('knowledge_area.id'))
    knowledge_area = relationship("KnowledgeAreas", back_populates="academic_program")

