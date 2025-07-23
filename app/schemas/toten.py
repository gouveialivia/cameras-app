from typing import Optional

from pydantic import BaseModel

class TotenCreate(BaseModel):
    nome1: str
    nome2: str
    latitude: float
    longitude: float
    descricao: str

class TotenResponse(BaseModel):
    id: int
    nome1: str
    nome2: str
    latitude: float
    longitude: float
    descricao: Optional[str] = None

    class Config:
        from_attributes = True

class TotenUpdate (BaseModel):
    nome1: str
    nome2: str
    latitude: float
    longitude: float
    descricao: str