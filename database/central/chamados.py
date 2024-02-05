from sqlalchemy import Column, Integer, String, DateTime, func, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, configure_metadata


class ChamadosORM(Base):
    metadata = configure_metadata()
    __tablename__ = 'chamados'

    id = Column(Integer, primary_key=True, index=True)
    created_by = Column(BigInteger)
    descricao = Column(String(255), nullable=False)
    tipo = Column(String(255), nullable=False)
    status = Column(String(50), nullable=True)
    updated_at = Column(DateTime, default=func.now(),
                        onupdate=func.now(), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
