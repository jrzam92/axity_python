# src/modulo_solid/adapters.py
import sqlite3
from .domain import User

class InMemoryUserRepository:
    def __init__(self):
        self._users: dict[int, User] = {}

    def save(self, user: User) -> None:
        self._users[user.id] = user

    def get_by_id(self, user_id: int) -> User | None:
        return self._users.get(user_id)


class SQLiteUserRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self._init_db()

    def _init_db(self):
        # Creamos la tabla si no existe
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)"
        )
        self.conn.commit()

    def save(self, user: User) -> None:
        # Insertamos el usuario o lo actualizamos
        self.conn.execute(
            "INSERT OR REPLACE INTO users (id, name, email) VALUES (?, ?, ?)",
            (user.id, user.name, user.email)
        )
        self.conn.commit()

    def get_by_id(self, user_id: int) -> User | None:
        # Buscamos al usuario por su ID
        cursor = self.conn.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        
        if row:
            return User(id=row[0], name=row[1], email=row[2])
        return None