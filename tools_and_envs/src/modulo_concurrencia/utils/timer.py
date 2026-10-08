import time
import functools
from typing import Callable

def timer(func: Callable):
    """Decorador para medir tiempo de ejecución"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed = end - start
        print(f"⏱️  {func.__name__}: {elapsed:.4f} segundos")
        return result
    return wrapper

def async_timer(func: Callable):
    """Decorador para medir tiempo de funciones async"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        end = time.perf_counter()
        elapsed = end - start
        print(f"⏱️  {func.__name__}: {elapsed:.4f} segundos")
        return result
    return wrapper

class TimerContext:
    """Context manager para medir bloques de código"""
    def __init__(self, name: str = "Bloque"):
        self.name = name
        self.start = None
    
    def __enter__(self):
        self.start = time.perf_counter()
        return self
    
    def __exit__(self, *args):
        elapsed = time.perf_counter() - self.start
        print(f"⏱️  {self.name}: {elapsed:.4f} segundos")