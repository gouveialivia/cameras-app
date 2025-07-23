from pydantic import BaseModel, EmailStr

class UsuarioBase(BaseModel):
    username: str
    password: str
    nome: str
    email: EmailStr
    celular: int
    endereco: str
    cep: int
    data_de_nascimento: str
class UsuarioRegister(BaseModel):
    username: str
    password: str
    nome: str
    email: EmailStr
    celular: int
    endereco: str
    cep: int
    data_de_nascimento: str
    
class UsuarioResponse(UsuarioRegister):
    id: int
    username: str
    password: str
    nome: str
    email: EmailStr
    celular: int
    endereco: str
    cep: int
    data_de_nascimento: str
    class Config:
        from_attributes = True
