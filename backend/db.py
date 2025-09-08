from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Modifica user:password@host:port/dbname con le tue credenziali PostgreSQL
DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/aiagentemail"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
