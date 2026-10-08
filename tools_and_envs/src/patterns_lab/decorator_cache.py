# src/patterns_lab/decorator_cache.py
from typing import Callable, Any

def simple_cache(func: Callable) -> Callable:
    """Decorador idiomático de Python para cachear resultados."""
    cache = {}

    def wrapper(*args, **kwargs) -> Any:
        # Creamos una clave única basada en los argumentos
        key = str(args) + str(kwargs)
        if key in cache:
            print("Retornando desde el caché...")
            return cache[key]
        
        print("Calculando y guardando en caché...")
        result = func(*args, **kwargs)
        cache[key] = result
        return result

    return wrapper

# Función de prueba que simula un cálculo pesado
@simple_cache
def expensive_computation(x: int, y: int) -> int:
    return x + y