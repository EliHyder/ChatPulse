from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from DB.models import Base, User, Message
from passlib.context import CryptContext

# Configura o contexto do passlib para usar o algoritmo bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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

def hash_password(password: str) -> str:
    """Gera o hash seguro da senha antes de salvar no banco."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara a senha digitada pelo usuário com o hash salvo no banco."""
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db, name: str, email: str, password: str):
    """
    Cria um novo usuário no banco de dados.
    """
    try:
        hashed_password = hash_password(password)
        new_user = User(name=name, email=email, password=hashed_password)
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise ValueError("Email already exists.")
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Error creating user: {str(e)}")

def verify_user(db, email: str, password: str):
    """
    Verifica se o usuário existe e se a senha está correta.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise ValueError("User not found.")
    if not verify_password(password, user.password):
        raise ValueError("Invalid password.")
    return user

def create_message(db, sender_id: int, recipient_id: int, body: str):
    """
    Cria uma nova mensagem no banco de dados.
    """
    try:
        new_message = Message(sender_id=sender_id, recipient_id=recipient_id, body=body)
        
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        return new_message
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Error creating message: {str(e)}")

def get_messages_for_user(db, user_id: int):
    """
    Retorna todas as mensagens enviadas e recebidas por um usuário específico.
    """
    try:
        sent_messages = db.query(Message).filter(Message.sender_id == user_id).all()
        received_messages = db.query(Message).filter(Message.recipient_id == user_id).all()
        return {
            "sent": sent_messages,
            "received": received_messages
        }
    except SQLAlchemyError as e:
        raise RuntimeError(f"Error retrieving messages: {str(e)}")

def get_message_send_receive(db, sender_id: int, recipient_id: int):
    """
    Retorna todas as mensagens enviadas de um usuário para outro.
    """
    try:
        messages_sent = db.query(Message).filter(
            Message.sender_id == sender_id,
            Message.recipient_id == recipient_id
        ).all()
        messages_received = db.query(Message).filter(
            Message.sender_id == recipient_id,
            Message.recipient_id == sender_id
        ).all()
        return {
            "sent": messages_sent,
            "received": messages_received
        }
    except SQLAlchemyError as e:
        raise RuntimeError(f"Error retrieving messages: {str(e)}")

