from pydantic import BaseModel


class Categorias(BaseModel):
    name: str    
class CategoriasResponse(Categorias):
    id: int