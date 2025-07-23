from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from app.models.usuario import Usuario

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def criar_token_acesso(username: str):
    #expira_em = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username} #, "exp": expira_em
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def authenticate(username: str, password: str, db: Session):
    usuario = db.query(Usuario).filter(Usuario.username == username).first()
    if not usuario:
        return None
    if usuario.password != password:  
        return None
    return usuario