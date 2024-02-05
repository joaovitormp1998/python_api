from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base, configure_metadata

class UsersORM(Base):
    metadata = configure_metadata() 
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, index = True)
    perfil_id = Column(Integer)
    username = Column(String)
    password = Column(String)
    nome = Column(String)
    last_name = Column(String)
    phone = Column(String)
    acesso = Column(DateTime, default=func.now())
    facebook_uid = Column(String)
    email_verified_at = Column(DateTime)
    remember_token = Column(String)
    created_token_at = Column(DateTime)
    root = Column(Integer, default=0)
    affiliate = Column(Integer)
