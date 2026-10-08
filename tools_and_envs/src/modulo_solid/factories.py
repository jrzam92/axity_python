# src/modulo_solid/factories.py
import sqlite3
from .domain import UserService
from .adapters import InMemoryUserRepository, SQLiteUserRepository

def user_service_factory(environment: str = "produccion") -> UserService:
    """
    Construye y devuelve un UserService inyectándole la dependencia
    correcta según el entorno en el que estemos trabajando.
    """
    if environment == "test":
        # Para pruebas, usamos la memoria (rápido y no deja basura)
        repository = InMemoryUserRepository()
    else:
        # Para desarrollo/producción, usamos SQLite
        # Nota: Aquí usamos una BD en memoria temporal para el ejemplo, 
        # pero en la vida real sería un archivo como "app.db"
        connection = sqlite3.connect(":memory:") 
        repository = SQLiteUserRepository(connection)
        
    # Inyectamos el repositorio al servicio (Inyección de dependencias)
    return UserService(repo=repository)