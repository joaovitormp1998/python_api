from sqlalchemy import Column, Integer, DECIMAL, String, JSON, ForeignKey, DateTime, func
from database import Base, configure_metadata

from sqlalchemy.orm import relationship

class PlansORM(Base):
    metadata = configure_metadata() 
    __tablename__ = 'plans'

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    description = Column(String)
    price = Column(DECIMAL)
    max_students = Column(Integer)
    max_storage = Column(Integer)
    is_active = Column(Integer)
    max_students = Column(Integer)    
    created_at = Column(DateTime, default = func.now())
    updated_at = Column(DateTime, onupdate = func.now())
    deleted_at = Column(DateTime)
    extra_storage = Column(DECIMAL)
    extra_students = Column(DECIMAL)
