from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import database_settings



engine = create_engine(database_settings.DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()