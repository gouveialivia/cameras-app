from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from app.auth.jwt import criar_token_acesso, authenticate
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.jwt import oauth2_scheme
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.camera import CameraCreate, CameraResponse, CameraUpdate
from app.models.camera import Camera
from app.schemas.token import TokenResponse
from app.schemas.toten import TotenCreate, TotenResponse, TotenUpdate
from app.models.toten import Toten
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioResponse, UsuarioRegister

router = APIRouter()
protected_router = APIRouter(prefix="/api", dependencies=[Depends(oauth2_scheme)])

@router.post("/registrar", response_model=UsuarioResponse, tags=["Usuario"])
def registrar(usuario: UsuarioRegister, db: Session = Depends(get_db)):
    existe = db.query(Usuario).filter(Usuario.username == usuario.username).first()
    if existe:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    novo_usuario = Usuario(username=usuario.username, password=usuario.password)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@protected_router.get("/usuarios/{id}", response_model=UsuarioResponse, tags=["Usuario"])
def pegar(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@router.post("/login", response_model=TokenResponse, tags=["Usuario"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not authenticate(username=form_data.username, password=form_data.password):
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    token = criar_token_acesso(form_data.username)
    return TokenResponse(access_token=token, token_type="bearer")

@protected_router.post("/cameras", response_model=CameraResponse, tags=["Camera"])
def criar_camera(cameracreate: CameraCreate, db: Session = Depends(get_db)):
    nova_camera = Camera(nome=cameracreate.nome, toten_id=cameracreate.toten_id)
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

@protected_router.post("/toten", response_model=TotenResponse, tags=["Toten"])
def criar_toten(totenbase: TotenCreate, db: Session = Depends(get_db)):
    novo_toten = Toten(nome1 = totenbase.nome1, nome2 = totenbase.nome2,
                       latitude = totenbase.latitude, longitude= totenbase.longitude,
                       descricao=totenbase.descricao)
    db.add(novo_toten)
    db.commit()
    db.refresh(novo_toten)
    return novo_toten

@protected_router.put("/toten/{id}", response_model=TotenResponse, tags=["Toten"])
def atualizar_toten(id: int, totenupdate: TotenUpdate, db: Session = Depends(get_db)):
    toten = db.query(Toten).filter(Toten.id == id).first()
    if not toten:
        raise HTTPException(status_code=404, detail="Toten não encontrado")
    toten.nome1 = totenupdate.nome1
    toten.nome2 = totenupdate.nome2
    toten.latitude = totenupdate.latitude
    toten.longitude = totenupdate.longitude
    toten.descricao = totenupdate.descricao
    try:
        db.commit()
        db.refresh(toten)
        return toten
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao atualizar toten")

@protected_router.delete("/toten/{id}", tags=["Toten"])
def deletar_toten(id: int, db: Session = Depends(get_db)):
    toten = db.query(Toten).filter(Toten.id == id).first()
    if not toten:
        raise HTTPException(status_code=404, detail="Toten não encontrado")
    try:
        db.delete(toten)
        db.commit()
        return {"detail": f"Toten com id {id} deletado com sucesso"}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao deletar toten")

@protected_router.get("/toten/{id}", response_model=TotenResponse, tags=["Toten"])
def pegar_toten(id: int, db: Session = Depends(get_db)):
    toten = db.query(Toten).filter(Toten.id == id).first()
    if not toten:
        raise HTTPException(status_code=404, detail="Toten não encontrado")
    return toten
