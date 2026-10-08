from src.clean_orders.application.use_cases import CreateOrderUseCase
from src.clean_orders.infrastructure.uow import InMemoryUnitOfWork
from src.clean_orders.infrastructure.presenters import APIPresenter

def test_create_order_use_case():
    # 1. Preparamos las dependencias (Infraestructura)
    uow = InMemoryUnitOfWork()
    presenter = APIPresenter()
    
    # 2. Inyectamos las dependencias en el caso de uso
    use_case = CreateOrderUseCase(uow=uow, presenter=presenter)
    
    # 3. Ejecutamos el caso de uso
    result = use_case.execute(order_id="ORD-001", amount=250.0)
    
    # 4. Validamos que el Presenter formateó bien la respuesta
    assert result["status"] == "success"
    assert result["data"]["order_id"] == "ORD-001"
    
    # 5. Validamos que el UoW hizo commit y guardó la entidad
    assert uow.committed is True
    assert "ORD-001" in uow.orders._orders