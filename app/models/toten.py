from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.db.database import Base

class Toten(Base):
    __tablename__ = "totens"

    id = Column(Integer, primary_key=True, index=True)
    nome1 = Column(String, nullable=False)
    nome2 = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    descricao = Column(String, nullable=True)

    cameras = relationship("Camera", back_populates="toten")
