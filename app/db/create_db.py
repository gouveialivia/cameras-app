from app.db.database import Base, engine

from app.models.camera import Camera
from app.models.usuario import Usuario
from app.models.toten import Toten
from app.models.mensagem import Mensagem
from app.models.feed import Postagem

def criar_tabelas():
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    criar_tabelas()
