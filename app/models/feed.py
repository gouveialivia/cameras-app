from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class Postagem(Base):
    __tablename__ = "postagens"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    texto = Column(Text, nullable=False)
    imagem_url = Column(String, nullable=True)
    localizacao = Column(String, nullable=True)
    cep = Column(String, nullable=True)
    votos_importante = Column(Integer, default=0)
    votos_nao_importante = Column(Integer, default=0)

    usuario = relationship("Usuario", back_populates="postagens")
