from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioResponse, UsuarioRegister
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.jwt import oauth2_scheme
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.token import TokenResponse
from app.auth.jwt import criar_token_acesso, authenticate

router = APIRouter()
protected_router = APIRouter(prefix="/api", dependencies=[Depends(oauth2_scheme)])

@router.post("/registrar", response_model=UsuarioResponse, tags=["Usuario"])
def registrar(usuario: UsuarioRegister, db: Session = Depends(get_db)):
    existe_usuario = db.query(Usuario).filter(Usuario.username == usuario.username).first()
    if existe_usuario:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    existe_email = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existe_email:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    novo_usuario = Usuario(username=usuario.username, password=usuario.password,  
        nome=usuario.nome, email=usuario.email, celular=usuario.celular,
        endereco=usuario.endereco, cep=usuario.cep, data_de_nascimento=usuario.data_de_nascimento)
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
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    usuario = authenticate(username=form_data.username, password=form_data.password, db=db)
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    token = criar_token_acesso(form_data.username)
    return TokenResponse(access_token=token, token_type="bearer")