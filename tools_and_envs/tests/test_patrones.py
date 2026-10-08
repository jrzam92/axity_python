import pytest
from src.design_patterns_lab.patrones import (
    Order, RegularPricing, VIPDiscountPricing,
    expensive_computation,
    LegacySMSProvider, LegacySMSAdapter
)

# --- Tests para Strategy ---
def test_regular_pricing():
    order = Order(amount=100.0, pricing_strategy=RegularPricing())
    assert order.checkout() == 100.0

def test_vip_discount_pricing():
    order = Order(amount=100.0, pricing_strategy=VIPDiscountPricing())
    assert order.checkout() == 80.0

# --- Tests para Decorator ---
def test_cache_decorator(mocker):
    # Usamos mocker (pytest-mock) o simplemente espiamos el comportamiento.
    # Como la función multiplica x * y:
    assert expensive_computation(5, 5) == 25
    assert expensive_computation(5, 5) == 25 
    
    # La caché debería guardar los resultados. El docstring debe mantenerse 
    # gracias a @wraps
    assert expensive_computation.__doc__ == "Simula una operación costosa."

# --- Tests para Adapter ---
def test_adapter_success():
    legacy_api = LegacySMSProvider()
    adapter = LegacySMSAdapter(legacy_api)
    
    # Probamos la interfaz que nuestra app conoce (.send)
    result = adapter.send(message="Hola Mundo", recipient="555-1234")
    assert result is True

def test_adapter_failure():
    legacy_api = LegacySMSProvider()
    adapter = LegacySMSAdapter(legacy_api)
    
    # Si falta el teléfono, el proveedor viejo falla, el adapter debe devolver False
    result = adapter.send(message="Hola Mundo", recipient="")
    assert result is False