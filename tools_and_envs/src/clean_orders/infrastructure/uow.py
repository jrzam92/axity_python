from src.clean_orders.application.interfaces import UnitOfWork, OrderRepository
from src.clean_orders.domain.entities import Order

class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self._orders = {}

    def add(self, order: Order) -> None:
        self._orders[order.id] = order

class InMemoryUnitOfWork(UnitOfWork):
    def __init__(self):
        self.orders = InMemoryOrderRepository()
        self.committed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # En SQLAlchemy aquí harías session.rollback() si hay error
        pass

    def commit(self) -> None:
        self.committed = True
        print("\n[UoW]: Transacción comiteada en base de datos (en memoria).")