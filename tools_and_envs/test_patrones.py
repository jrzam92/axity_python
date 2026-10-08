import pytest

# Importamos desde tu nuevo módulo dentro de src
from design_patterns_lab.patrones import (
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
def test_cache_decorator():
    # Primera llamada (calcula y guarda en caché)
    assert expensive_computation(5, 5) == 25
    # Segunda llamada (retorna de la caché)
    assert expensive_computation(5, 5) == 25 
    
    # Verificamos que @wraps conservó la metadata de la función
    assert expensive_computation.__doc__ == "Simula una operación costosa."

# --- Tests para Adapter ---
def test_adapter_success():
    legacy_api = LegacySMSProvider()
    adapter = LegacySMSAdapter(legacy_api)
    
    result = adapter.send(message="Hola Mundo", recipient="555-1234")
    assert result is True

def test_adapter_failure():
    legacy_api = LegacySMSProvider()
    adapter = LegacySMSAdapter(legacy_api)
    
    result = adapter.send(message="Hola Mundo", recipient="")
    assert result is False