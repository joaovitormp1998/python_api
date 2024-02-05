from pydantic import BaseModel
from typing import Dict, Optional


class PaymentSettings(BaseModel):
    descricao_na_fatura: str
    parcelamento_cartao_recorrente: str
    parcelamento_cartao: str
    parcelamento_boleto: str
    dias_vencimento_boleto: int
    dias_bloqueio_curso: int
    dias_bloqueio_extensao: int
    valor_minimo_parcela: float
    taxa_imposto: float
    habilitar_solicitacao_bolsa: bool
    aceitar_boleto_bancario: bool
    aceitar_pix: bool
    aceitar_cartao_credito: bool
    aceitar_cartao_credito_recorrente: bool
    gateway_id: Optional[str]
    gateway_configuration: Optional[Dict]


class PaymentSettingsResponse(PaymentSettings):
    id: int
