from pydantic import BaseModel, Field

class CameraBase(BaseModel):
    nome: str
    ip: str 

class CameraCreate(CameraBase):
    toten_id: int

class CameraUpdate(CameraBase):
    toten_id: int

class CameraResponse(CameraBase):
    id: int
    toten_id: int
    class Config:
        from_attributes = True
