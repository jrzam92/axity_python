from .interfaces import UnitOfWork, Presenter
from src.clean_orders.domain.entities import Order
from src.clean_orders.domain.events import OrderCreated

class CreateOrderUseCase:
    def __init__(self, uow: UnitOfWork, presenter: Presenter):
        self.uow = uow
        self.presenter = presenter

    def execute(self, order_id: str, amount: float) -> dict:
        # 1. Instanciamos la entidad y ejecutamos su lógica
        order = Order(id=order_id, amount=amount)
        order.create()

        # 2. Transacción gestionada por el Unit of Work
        with self.uow:
            self.uow.orders.add(order)
            self.uow.commit()  # Si esto falla, no hay commit.

        # 3. Manejo de Eventos (Aquí lo hacemos de forma simple en la app)
        for event in order.events:
            self._handle_event(event)

        # 4. Formatear salida con el Presenter
        return self.presenter.present_success(order.id)

    def _handle_event(self, event: any):
        """Simula un manejador de eventos dentro de la aplicación."""
        if isinstance(event, OrderCreated):
            # En la vida real, aquí enviarías un email, notificarías a otra API, etc.
            print(f"\n[EVENTO MANEJADO]: Notificando al almacén sobre la orden {event.order_id}")