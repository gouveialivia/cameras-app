from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    toten_id = Column(Integer, ForeignKey("totens.id"))
    ip = Column(String, nullable=False)

    toten = relationship("Toten", back_populates="cameras")