from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DB.models import Base

# Caminho do banco de dados SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./chatpulse.db"

# Cria o motor do SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Fábrica de sessões para as requisições
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency para injetar a sessão do banco de dados nas rotas do FastAPI.
    Garante que a sessão será fechada após o uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Cria as tabelas no banco de dados com base nos modelos definidos.
    """
    Base.metadata.create_all(bind=engine)