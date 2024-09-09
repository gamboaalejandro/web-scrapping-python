import uuid

from sqlalchemy import Column, String, Text, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from data.models.database import Base

"""
Class for save institute data 
"""

university_knowledge_association = Table(
    'university_knowledge_association', Base.metadata,
    Column('university_id', UUID(as_uuid=True), ForeignKey('University.id'), primary_key=True),
    Column('knowledge_area_id', UUID(as_uuid=True), ForeignKey('knowledge_area.id'), primary_key=True)

)


class UniversityInstitute(Base):
    #better name for tablename
    __tablename__ = 'University'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    university_name = Column(Text, nullable=False)

    knowledge_areas = relationship(
        'KnowledgeAreas',
        secondary=university_knowledge_association,
        back_populates='universities'
    )

