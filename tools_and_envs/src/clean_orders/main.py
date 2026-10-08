from fastapi import FastAPI
from pydantic import BaseModel

# Importamos nuestras piezas de Arquitectura Limpia
from src.clean_orders.infrastructure.uow import InMemoryUnitOfWork
from src.clean_orders.infrastructure.presenters import APIPresenter
from src.clean_orders.application.use_cases import CreateOrderUseCase

app = FastAPI(title="Clean Architecture Orders API")

# Definimos cómo esperamos recibir los datos del cliente
class OrderRequest(BaseModel):
    order_id: str
    amount: float

@app.post("/orders", status_code=201)
def create_order(request: OrderRequest):
    # 1. Instanciamos la infraestructura (idealmente esto lo hace un inyector de dependencias)
    uow = InMemoryUnitOfWork()
    presenter = APIPresenter()
    
    # 2. Armamos el caso de uso pasándole la infraestructura
    use_case = CreateOrderUseCase(uow=uow, presenter=presenter)
    
    # 3. Ejecutamos la lógica de negocio purita
    result = use_case.execute(order_id=request.order_id, amount=request.amount)
    
    # 4. Retornamos lo que el Presenter nos formateó
    return result