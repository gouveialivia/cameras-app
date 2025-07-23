from app.db.database import Base, engine

# Importa todos os models para registrar as tabelas
from app.models.camera import Camera
from app.models.usuario import Usuario
from app.models.toten import Toten
from app.models.mensagem import Mensagem

def criar_tabelas():
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    criar_tabelas()
