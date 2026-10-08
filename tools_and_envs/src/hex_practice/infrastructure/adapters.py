from hex_practice.domain.entities import Order
from hex_practice.domain.ports import OrderRepository, NotificationAdapter

# --- Adaptador 1: En Memoria (Ideal para testing rápido) ---
class InMemoryOrderRepository:
    def __init__(self):
        self._db = {}

    def save(self, order: Order) -> None:
        self._db[order.id] = order

    def get_by_id(self, order_id: str) -> Order:
        return self._db.get(order_id)

# --- Adaptador 2: Notificador HTTP Simulado ---
class MockHttpNotificationAdapter:
    def send_notification(self, message: str) -> None:
        print(f"[HTTP POST simulado] Enviando: {message}")

# Nota: El adaptador de SQLAlchemy sería otra clase (ej. SQLAlchemyOrderRepository)
# que reciba una sesión de BD y convierta el modelo de SQLAlchemy en la Entidad pura.