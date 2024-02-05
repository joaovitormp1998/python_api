from sqlalchemy import Column, Integer, BigInteger, DECIMAL, String, JSON, ForeignKey, DateTime, func, FLOAT
from database import Base, configure_metadata

from sqlalchemy.orm import relationship


class ProductInvoiceORM(Base):
    metadata = configure_metadata()
    __tablename__ = 'product_invoice'

    id = Column(Integer, primary_key=True, index=True)
    categoria = Column(String, index=True)
    nome = Column(String, index=True)
    unidade_de_medida = Column(String)
    valor = Column(DECIMAL)


class OrdemServicoORM(Base):
    metadata = configure_metadata()
    __tablename__ = 'ordem_servico'
    id = Column(BigInteger, primary_key=True, index=True)
    company_id = Column(BigInteger)
    created_at = Column(DateTime)
    stripe_pagamento_id = Column(String, index=True)
    updated_at = Column(DateTime)
    tipo_cliente = Column(String, index=True)
    informacoes_do_servico = Column(String, index=True)
    categoria = Column(String, index=True)
    status = Column(String, index=True)
    contrato = Column(String, index=True)
    pagamento = Column(String, index=True)
    user_id = Column(BigInteger)
    imposto_percentual = Column(DECIMAL)
    desconto_percentual = Column(DECIMAL)
    total = Column(FLOAT)


class OrdemServicoProductInvoiceORM(Base):
    metadata = configure_metadata()
    __tablename__ = 'ordem_servico_product_invoice'
    ordem_servico_id = Column(BigInteger, primary_key=True, index=True)
    product_invoice_id = Column(Integer, primary_key=True, index=True)
