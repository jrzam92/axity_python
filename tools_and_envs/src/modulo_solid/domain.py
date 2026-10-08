# src/modulo_solid/domain.py
from dataclasses import dataclass
from typing import Protocol

# 1. Entidad de Dominio (SRP: Su única responsabilidad es representar datos)
@dataclass
class User:
    id: int
    name: str
    email: str

# 2. El Puerto / Abstracción (ISP y DIP)
# Usamos Protocol para definir qué debe hacer un repositorio, sin importar cómo lo haga.
class UserRepository(Protocol):
    def save(self, user: User) -> None:
        ...

    def get_by_id(self, user_id: int) -> User | None:
        ...

# 3. El Servicio (Inyección de dependencias)
# Depende de UserRepository (la abstracción), no de SQLite o Memoria.
class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register_user(self, id: int, name: str, email: str) -> User:
        # Regla de negocio: no pueden existir dos usuarios con el mismo ID
        if self.repo.get_by_id(id):
            raise ValueError(f"El usuario con id {id} ya existe.")
        
        new_user = User(id=id, name=name, email=email)
        self.repo.save(new_user)
        return new_user