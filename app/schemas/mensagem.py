from pydantic import BaseModel
from datetime import datetime

class MensagemBase(BaseModel):
    mensagem: str

class MensagemCreate(MensagemBase):
    usuario_id: int 

class MensagemUpdate(MensagemBase):
    mensagem: str

class MensagemOut(MensagemBase):
    id: int
    usuario_id: int
    created_at: datetime

    class Config:
        from_attributes = True