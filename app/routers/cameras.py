from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.camera import CameraCreate, CameraResponse, CameraUpdate
from app.models.camera import Camera
from sqlalchemy.exc import SQLAlchemyError
from app.auth.jwt import oauth2_scheme

router = APIRouter()
protected_router = APIRouter(prefix="/api", dependencies=[Depends(oauth2_scheme)])


@protected_router.post("/cameras", response_model=CameraResponse, tags=["Camera"])
def criar_camera(cameracreate: CameraCreate, db: Session = Depends(get_db)):
    nova_camera = Camera(nome=cameracreate.nome, ip=cameracreate.ip, toten_id=cameracreate.toten_id)
    db.add(nova_camera)
    db.commit()
    db.refresh(nova_camera)
    return nova_camera

@protected_router.put("/cameras/{id}", response_model=CameraResponse, tags=["Camera"])
def atualizar_camera(id: int, cameraupdate: CameraUpdate, db: Session = Depends(get_db)):
    camera = db.query(Camera).filter(Camera.id == id).first()
    if not camera:
        raise HTTPException(status_code=404, detail="Câmera não encontrada")
    camera.nome = cameraupdate.nome
    camera.ip = cameraupdate.ip
    camera.toten_id = cameraupdate.toten_id
    db.commit()
    db.refresh(camera)
    return camera

@protected_router.delete("/cameras/{id}", tags=["Camera"])
def deletar_camera(id: int, db: Session = Depends(get_db)):
    camera = db.query(Camera).filter(Camera.id == id).first()
    if not camera:
        raise HTTPException(status_code=404, detail="Câmera não encontrada")
    try:
        db.delete(camera)
        db.commit()
        return {"detail": "Câmera deletada com sucesso"}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao deletar câmera")

@protected_router.get("/cameras/{id}", response_model=CameraResponse, tags=["Camera"])
def pegar_camera(id: int, db: Session = Depends(get_db)):
    camera = db.query(Camera).filter(Camera.id == id).first()
    if not camera:
        raise HTTPException(status_code=404, detail="Câmera não encontrada")
    return camera