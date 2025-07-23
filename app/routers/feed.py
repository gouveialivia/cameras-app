from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import get_db
from app.auth.jwt import oauth2_scheme, get_current_user
from app.models.feed import Postagem
from app.schemas.feed import PostagemCreate, PostagemOut, PostagemUpdate

router = APIRouter()
protected_router = APIRouter(prefix="/api", dependencies=[Depends(oauth2_scheme)])

@protected_router.post("/postagens", response_model=PostagemOut, tags=["Postagem"])
def criar_postagem(
    post: PostagemCreate,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
):
    try:
        nova_postagem = Postagem(texto=post.texto, imagem_url=post.imagem_url,
                                localizacao=post.localizacao, cep=post.cep,
                                usuario_id=usuario.id)
        db.add(nova_postagem)
        db.commit()
        db.refresh(nova_postagem)
        return nova_postagem
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao criar postagem")

@protected_router.get("/postagens/{id}", response_model=PostagemOut, tags=["Postagem"])
def obter_postagem(id: int, db: Session = Depends(get_db)):
    postagem = db.query(Postagem).filter(Postagem.id == id).first()
    if not postagem:
        raise HTTPException(status_code=404, detail="Postagem não encontrada")
    return postagem


@protected_router.get("/postagens", response_model=list[PostagemOut], tags=["Postagem"])
def listar_postagens(db: Session = Depends(get_db)):
    return db.query(Postagem).all()

@protected_router.put("/postagens/{id}", response_model=PostagemOut, tags=["Postagem"])
def atualizar_postagem(id: int, post: PostagemUpdate, db: Session = Depends(get_db)):
    postagem = db.query(Postagem).filter(Postagem.id == id).first()
    if not postagem:
        raise HTTPException(status_code=404, detail="Postagem não encontrada")
    postagem.texto = post.texto
    postagem.imagem_url = post.imagem_url
    postagem.localizacao = post.localizacao
    postagem.cep = post.cep
    db.commit()
    db.refresh(postagem)
    return postagem

@protected_router.delete("/postagens/{id}", tags=["Postagem"])
def deletar_postagem(id: int, db: Session = Depends(get_db)):
    postagem = db.query(Postagem).filter(Postagem.id == id).first()
    if not postagem:
        raise HTTPException(status_code=404, detail="Postagem não encontrada")
    try:
        db.delete(postagem)
        db.commit()
        return {"detail": "Postagem deletada com sucesso"}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao deletar postagem")