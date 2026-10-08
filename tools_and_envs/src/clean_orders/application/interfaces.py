from abc import ABC, abstractmethod
from src.clean_orders.domain.entities import Order

class OrderRepository(ABC):
    @abstractmethod
    def add(self, order: Order) -> None:
        pass

class UnitOfWork(ABC):
    """El Unit of Work maneja las transacciones. 
    Actúa como un context manager (with...)."""
    orders: OrderRepository

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

class Presenter(ABC):
    """Interfaz para formatear la salida hacia el exterior (API, Consola, etc)."""
    @abstractmethod
    def present_success(self, order_id: str) -> dict:
        pass