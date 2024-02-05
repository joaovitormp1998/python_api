from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime, func
from database import Base, configure_metadata

from sqlalchemy.orm import relationship

class LinktreeLinkORM(Base):
    metadata = configure_metadata() 
    __tablename__ = 'linktrees_links'

    id = Column(Integer, primary_key = True, index = True)
    linktree_id = Column(Integer)
    social_name = Column(String)
    social_link = Column(String)
