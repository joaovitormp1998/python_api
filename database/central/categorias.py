from sqlalchemy import Column, Integer, DECIMAL, String, JSON, ForeignKey, DateTime, func
from database import Base, configure_metadata

from sqlalchemy.orm import relationship

class CategoriasORM(Base):
    metadata = configure_metadata() 
    __tablename__ = 'category_products'

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default = func.now())
    updated_at = Column(DateTime, onupdate = func.now())
    deleted_at = Column(DateTime)
