from hex_practice.domain.entities import Order
from hex_practice.domain.ports import OrderRepository, NotificationAdapter
from .dtos import CreateOrderRequest, CreateOrderResponse

class CreateOrderUseCase:
    # Inyección de dependencias a través del constructor
    def __init__(self, repo: OrderRepository, notifier: NotificationAdapter):
        self.repo = repo
        self.notifier = notifier

    def execute(self, request: CreateOrderRequest) -> CreateOrderResponse:
        # 1. Convertir DTO a Entidad de Dominio
        order = Order(item_name=request.item_name, quantity=request.quantity)
        
        # 2. Lógica delegada a los puertos
        self.repo.save(order)
        self.notifier.send_notification(f"Orden creada: {order.id}")
        
        # 3. Convertir Entidad a DTO de salida
        return CreateOrderResponse(order_id=order.id, status="CREATED")