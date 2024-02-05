from pydantic import BaseModel



class ProductInvoice(BaseModel):
    categoria: str
    nome: str
    unidade_de_medida: str
    valor:float

class ProductInvoiceResponse(ProductInvoice):
    id: int