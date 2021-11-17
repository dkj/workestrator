from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.operators import isnot_distinct_from

from .database import Base


class PipelineWork(Base):
    __tablename__ = "pipelinework"

    pipeline_id = Column(String, primary_key=True, index=True)
    unique = Column(String, primary_key=True, index=True)
    info = Column(String)
    state = Column(String, default="PENDING")

