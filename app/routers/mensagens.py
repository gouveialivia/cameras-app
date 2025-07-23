from fastapi import APIRouter, HTTPException, Depends
from app.auth.jwt import oauth2_scheme
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.mensagem import Mensagem
from app.schemas.mensagem import MensagemCreate, MensagemOut
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()
protected_router = APIRouter(prefix="/api", dependencies=[Depends(oauth2_scheme)])

@protected_router.post("/mensagens", response_model=MensagemOut, tags=["Mensagem"])
def criar_mensagem(mensagem: MensagemCreate, db: Session = Depends(get_db)):
    nova_mensagem = Mensagem(
        usuario_id=mensagem.usuario_id,  
        mensagem=mensagem.mensagem
    )
    try:
        db.add(nova_mensagem)
        db.commit()
        db.refresh(nova_mensagem)
        return nova_mensagem
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao criar mensagem")
    
@protected_router.get("/mensagens/{id}", response_model=MensagemOut, tags=["Mensagem"])
def pegar_mensagem(id: int, db: Session = Depends(get_db)):
    mensagem = db.query(Mensagem).filter(Mensagem.id == id).first()
    if not mensagem:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    return mensagem
