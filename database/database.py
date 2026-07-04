from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy
import os

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./contact.db")

if DB_URL.startswith("postgres://"):
    DB_URL = DB_URL.replace("postgres://", "postgresql://", 1)

if "sqlite" in DB_URL:
    engine = create_engine(DB_URL, connect_args={"check_same_thread": False, "timeout": 30})
else:
    engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()