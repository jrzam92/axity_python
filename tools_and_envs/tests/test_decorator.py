from patterns_lab.decorator_cache import expensive_computation

def test_cache_decorator():
    # La primera llamada debe calcular
    res1 = expensive_computation(5, 5)
    
    # La segunda llamada debe venir del caché (aunque aquí solo probamos el resultado lógico)
    res2 = expensive_computation(5, 5)
    
    # Si le pasamos parámetros diferentes, es un cálculo nuevo
    res3 = expensive_computation(10, 2)
    
    assert res1 == 10
    assert res2 == 10
    assert res3 == 12