from typing import Protocol
from .entities import Order

class OrderRepository(Protocol):
    """Puerto de salida: define CÓMO se guarda, pero no DÓNDE."""
    def save(self, order: Order) -> None:
        ...
    
    def get_by_id(self, order_id: str) -> Order:
        ...

class NotificationAdapter(Protocol):
    """Puerto de salida: define cómo notificar."""
    def send_notification(self, message: str) -> None:
        ...