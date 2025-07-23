from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.toten import TotenCreate, TotenResponse, TotenUpdate
from app.models.toten import Toten
from app.auth.jwt import oauth2_scheme

router = APIRouter()
protected_router = APIRouter(prefix="/api", dependencies=[Depends(oauth2_scheme)])

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
