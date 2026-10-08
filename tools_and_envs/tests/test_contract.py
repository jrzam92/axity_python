import pytest
from hex_practice.domain.entities import Order
from hex_practice.infrastructure.adapters import InMemoryOrderRepository

# Si tuvieras el adaptador de SQLAlchemy, lo agregarías a esta lista
@pytest.fixture(params=[InMemoryOrderRepository])
def repository(request):
    """Esta fixture ejecutará las pruebas para CADA adaptador que le pases."""
    RepoClass = request.param
    return RepoClass()

def test_repository_contract_saves_and_retrieves(repository):
    # Dado
    order = Order(item_name="Laptop", quantity=1)
    
    # Cuando
    repository.save(order)
    retrieved_order = repository.get_by_id(order.id)
    
    # Entonces
    assert retrieved_order is not None
    assert retrieved_order.id == order.id
    assert retrieved_order.item_name == "Laptop"