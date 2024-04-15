import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from models import Base

# Konfiguracja bazy danych w pamięci
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Tworzenie silnika bazy danych w pamięci
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Tworzenie sesji
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tworzenie bazy danych
Base.metadata.create_all(bind=engine)

# Fixtures

@pytest.fixture
def db():
    """
    Fixture do zarządzania sesją bazy danych.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(db):
    """
    Fixture do tworzenia klienta testowego.
    """
    def override_get_db():
        return db

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    return client