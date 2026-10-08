import math
import hashlib

def fibonacci_recursivo(n: int) -> int:
    """Fibonacci recursivo (ineficiente a propósito para simular CPU-bound)"""
    if n <= 1:
        return n
    return fibonacci_recursivo(n - 1) + fibonacci_recursivo(n - 2)

def es_primo(n: int) -> bool:
    """Verifica si un número es primo (CPU-intensive)"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def contar_primos(start: int, end: int) -> int:
    """Cuenta números primos en un rango"""
    return sum(1 for n in range(start, end) if es_primo(n))

def hash_intensivo(data: str, iterations: int = 100000) -> str:
    """Cálculo intensivo de hashes (CPU-bound)"""
    result = data.encode()
    for _ in range(iterations):
        result = hashlib.sha256(result).digest()
    return result.hex()