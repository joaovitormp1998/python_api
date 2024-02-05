from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from database import Base, configure_metadata
from sqlalchemy.orm import relationship

class AddressORM(Base):
    metadata = configure_metadata() 
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer)
    buyer_id = Column(Integer)
    zip_code = Column(String)
    country = Column(String(2))
    city = Column(String)
    state = Column(String(2))
    address_line = Column(String)
    address_line_2 = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.current_timestamp())
    neighborhood = Column(String)
    street = Column(String)
    number = Column(String)
