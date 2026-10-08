from fastapi import FastAPI, Depends
from hex_practice.application.dtos import CreateOrderRequest, CreateOrderResponse
from hex_practice.application.use_cases import CreateOrderUseCase
from hex_practice.infrastructure.adapters import InMemoryOrderRepository, MockHttpNotificationAdapter

app = FastAPI(title="Hexagonal Architecture API")

# --- Wiring (Inyección de Dependencias) ---
# Instanciamos los adaptadores. En un entorno real, la BD cambiaría según el entorno.
repo_adapter = InMemoryOrderRepository()
notifier_adapter = MockHttpNotificationAdapter()

def get_create_order_use_case() -> CreateOrderUseCase:
    return CreateOrderUseCase(repo=repo_adapter, notifier=notifier_adapter)

# --- Endpoint ---
@app.post("/orders", response_model=CreateOrderResponse)
def create_order(
    request: CreateOrderRequest, 
    use_case: CreateOrderUseCase = Depends(get_create_order_use_case)
):
    return use_case.execute(request)