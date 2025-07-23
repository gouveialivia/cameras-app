from pydantic import BaseModel

class UsuarioBase(BaseModel):
    username: str
    password: str

class UsuarioRegister(BaseModel):
    username: str
    password: str

class UsuarioResponse(UsuarioRegister):
    id: int
    class Config:
        from_attributes = True
