from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime, func
from database import Base, configure_metadata

from sqlalchemy.orm import relationship

class LinktreesORM(Base):
    metadata = configure_metadata() 
    __tablename__ = 'linktrees'

    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer)
    url = Column(String)
    name = Column(String)
    colorBackLink = Column(String)
    colorBackground = Column(String)
    colorName = Column(String)
    colorNameLink = Column(String)
    image = Column(String)
    created_at = Column(DateTime, default = func.now())
    updated_at = Column(DateTime, onupdate = func.now())
