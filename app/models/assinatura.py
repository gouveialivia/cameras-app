from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from app.db.database import Base

class Assinatura(Base):
    __tablename__ = "assinaturas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)

