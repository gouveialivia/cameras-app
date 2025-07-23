from fastapi import APIRouter, HTTPException, Depends
from app.auth.jwt import oauth2_scheme
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.mensagem import Mensagem
from app.schemas.mensagem import MensagemCreate, MensagemOut, MensagemUpdate
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

@protected_router.put("/mensagens/{id}", response_model=MensagemOut, tags=["Mensagem"])
def atualizar_mensagem(id: int, dados: MensagemUpdate, db: Session = Depends(get_db)):
    mensagem = db.query(Mensagem).filter(Mensagem.id == id).first()
    if not mensagem:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    if dados.mensagem is not None:
        mensagem.mensagem = dados.mensagem
    try:
        db.commit()
        db.refresh(mensagem)
        return mensagem
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao atualizar mensagem")

@protected_router.delete("/mensagens/{id}", response_model=MensagemOut, tags=["Mensagem"])
def deletar_mensagem(id: int, db: Session = Depends(get_db)):
    mensagem = db.query(Mensagem).filter(Mensagem.id == id).first()
    if not mensagem:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    
    try:
        db.delete(mensagem)
        db.commit()
        return mensagem
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao deletar mensagem")


