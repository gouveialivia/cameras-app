from sqlalchemy import Column, Integer, String
from app.db.database import Base
from sqlalchemy.orm import relationship


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    celular = Column(String, nullable=False)
    endereco = Column(String, nullable=False)
    cep = Column(String, nullable=False)
    data_de_nascimento = Column(String, nullable=False)

    mensagens = relationship("Mensagem", back_populates="usuario")