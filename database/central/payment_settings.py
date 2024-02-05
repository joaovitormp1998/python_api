from sqlalchemy import Column, Integer, String, Float, Boolean, JSON
from sqlalchemy.orm import relationship
from database import Base, configure_metadata


class PaymentSettingsORM(Base):
    metadata = configure_metadata()
    __tablename__ = 'payment_settings'

    id = Column(Integer, primary_key=True, index=True)
    descricao_na_fatura = Column(String, nullable=False)
    parcelamento_cartao_recorrente = Column(String)
    parcelamento_cartao = Column(String)
    parcelamento_boleto = Column(String)
    dias_vencimento_boleto = Column(Integer)
    dias_bloqueio_curso = Column(Integer)
    dias_bloqueio_extensao = Column(Integer)
    valor_minimo_parcela = Column(Float)
    taxa_imposto = Column(Float)
    habilitar_solicitacao_bolsa = Column(Boolean)
    aceitar_boleto_bancario = Column(Boolean)
    aceitar_pix = Column(Boolean)
    aceitar_cartao_credito = Column(Boolean)
    aceitar_cartao_credito_recorrente = Column(Boolean)
    gateway_id = Column(String, nullable=True)
    gateway_configuration = Column(JSON, nullable=True)
