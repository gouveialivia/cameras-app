from pydantic import BaseModel, validator


class CameraBase(BaseModel):
    nome: str

class CameraCreate(BaseModel):
    nome: str
    toten_id: str

class CameraResponse(BaseModel):
    id: int
    nome: str
    toten_id: int

    class Config:
        from_attributes = True

class CameraUpdate (BaseModel):
    nome: str
    toten_id: str