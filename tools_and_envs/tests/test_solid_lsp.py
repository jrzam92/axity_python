# tests/test_solid_lsp.py
import pytest
import sqlite3

# Importamos desde nuestra carpeta src
from src.modulo_solid.domain import User, UserRepository, UserService
from src.modulo_solid.adapters import InMemoryUserRepository, SQLiteUserRepository

# --- FIXTURE PARA EL PRINCIPIO DE LISKOV ---
@pytest.fixture(params=["memory", "sqlite"])
def repository(request) -> UserRepository:
    if request.param == "memory":
        return InMemoryUserRepository()
    elif request.param == "sqlite":
        conn = sqlite3.connect(":memory:")
        return SQLiteUserRepository(conn)

# --- TESTS ---
def test_repository_liskov_substitution(repository: UserRepository):
    """
    LSP: Este test correrá 2 veces (una por cada BD). Si ambas pasan,
    significa que podemos sustituir una por otra sin romper el sistema.
    """
    # Arrange (Preparar)
    user = User(id=1, name="Guido", email="guido@python.org")
    
    # Act (Actuar)
    repository.save(user)
    fetched_user = repository.get_by_id(1)
    missing_user = repository.get_by_id(99)
    
    # Assert (Comprobar)
    assert fetched_user is not None
    assert fetched_user.name == "Guido"
    assert missing_user is None


def test_user_service_registration():
    """
    Probamos el servicio usando la implementación en memoria (rápida).
    """
    repo = InMemoryUserRepository()
    service = UserService(repo)
    
    user = service.register_user(1, "Ada", "ada@lovelace.com")
    assert user.name == "Ada"
    
    # Comprobamos que lance el error de negocio esperado
    with pytest.raises(ValueError, match="ya existe"):
        service.register_user(1, "Otro", "otro@mail.com")