import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.modulo_fastapi.main import app
from src.modulo_fastapi.database import Base, get_db
from src.modulo_fastapi.services.auth_service import create_access_token

# DB en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    """Crea DB temporal para cada test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    """Cliente de test con DB temporal"""
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def auth_token():
    """Token JWT válido para tests"""
    return create_access_token(data={"sub": "admin"})

@pytest.fixture
def auth_headers(auth_token):
    """Headers con autenticación"""
    return {"Authorization": f"Bearer {auth_token}"}