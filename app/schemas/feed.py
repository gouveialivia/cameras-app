from pydantic import BaseModel
from typing import Optional

class PostagemBase(BaseModel):
    texto: str
    imagem_url: Optional[str] = None
    localizacao: Optional[str] = None
    cep: Optional[str] = None

class PostagemCreate(PostagemBase):
    pass

class PostagemOut(PostagemBase):
    id: int
    usuario_id: int
    votos_importante: int
    votos_nao_importante: int

    class Config:
        from_attributes = True

class PostagemUpdate(BaseModel):
    texto: Optional[str] = None
    imagem_url: Optional[str] = None
    localizacao: Optional[str] = None
    cep: Optional[str] = None
