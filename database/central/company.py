from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database import Base, configure_metadata
from sqlalchemy.orm import relationship

class CompanyORM(Base):
    metadata = configure_metadata() 
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    cargo_criador = Column(String(255))
    razao_social = Column(String(255))
    nome_fantasia = Column(String(255))
    cnpj = Column(String(18), unique=True)
    insc_estadual = Column(String(20))
    insc_municipal = Column(String(20))
    telefone = Column(String(15))
    email = Column(String(255))
    endereco = Column(String(255))
    numero = Column(String(10))
    complemento = Column(String(255))
    bairro = Column(String(255))
    cep = Column(String(10))
    cidade = Column(String(255))
    estado = Column(String(2))
    pais = Column(String(50))
    created_by = Column(Integer, ForeignKey('users.id'))  # Referenciando a tabela 'users'

    # Relação com a tabela 'users'
    users = relationship('UserORM', back_populates='company')