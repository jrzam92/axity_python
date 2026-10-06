import pytest
from unittest.mock import patch
from hypothesis import given, strategies as st
# Importaremos de un módulo que aún no hemos programado (TDD)
from src.pruebas_tdd.descuentos import calcular_total, notificar_cliente

# 1. Fixture: Nos da un escenario base repetible
@pytest.fixture
def carrito_pequeno():
    return [
        {"producto": "Teclado", "precio": 50.0},
        {"producto": "Mouse", "precio": 20.0}
    ] # Total base: 70.0

# 2. Parametrización y Markers
@pytest.mark.descuentos # Marker personalizado para agrupar pruebas
@pytest.mark.parametrize("es_vip, total_esperado", [
    (False, 70.0), # No cumple volumen, no es VIP -> Sin descuento
    (True, 66.5),  # 5% VIP de 70.0 -> Descuento de 3.5
])
def test_calcular_total_pequeno(carrito_pequeno, es_vip, total_esperado):
    assert calcular_total(carrito_pequeno, es_vip=es_vip) == total_esperado

def test_calcular_total_con_volumen():
    # 4 artículos a 10.0 cada uno = 40.0. Al ser >3 aplica 10% desc. -> 36.0
    carrito_grande = [{"precio": 10.0}] * 4 
    assert calcular_total(carrito_grande, es_vip=False) == 36.0

# 3. Mocking con unittest.mock
@patch("src.pruebas_tdd.descuentos.servicio_email_externo")
def test_notificar_cliente(mock_email):
    # Simulamos que el servicio de correo siempre responde True
    mock_email.return_value = True
    
    resultado = notificar_cliente("polux@test.com", "Tu pedido está listo")
    
    # Verificamos que nuestro código sí llamó al servicio externo correctamente
    mock_email.assert_called_once_with("polux@test.com", "Tu pedido está listo")
    assert resultado is True

# 4. Property-based testing (Hypothesis)
# Genera listas aleatorias de precios de forma automática para buscar errores raros
@given(precios=st.lists(st.floats(min_value=0.0, max_value=1000.0), max_size=50))
def test_total_nunca_es_negativo(precios):
    carrito = [{"precio": p} for p in precios]
    # No importa cuántos productos ni el precio, un total jamás debe dar negativo
    total = calcular_total(carrito, es_vip=True)
    assert total >= 0.0