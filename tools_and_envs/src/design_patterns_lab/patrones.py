from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable

# ==========================================
# 1. STRATEGY (Patrón de Comportamiento)
# ==========================================
# Objetivo: Intercambiar algoritmos de precios dinámicamente sin usar múltiples if/elif.

class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float:
        pass

class RegularPricing(PricingStrategy):
    def calculate(self, amount: float) -> float:
        return amount

class VIPDiscountPricing(PricingStrategy):
    def calculate(self, amount: float) -> float:
        return amount * 0.80  # 20% de descuento

# Usamos dataclasses (patrón idiomático en Python) para crear nuestra clase Contexto
@dataclass
class Order:
    amount: float
    pricing_strategy: PricingStrategy

    def checkout(self) -> float:
        return self.pricing_strategy.calculate(self.amount)


# ==========================================
# 2. DECORATOR (Patrón Idiomático / Estructural)
# ==========================================
# Objetivo: Añadir comportamiento de caché a una función sin modificar su código.

def cache_decorator(func: Callable) -> Callable:
    cache = {}
    
    @wraps(func) # Conserva el nombre y docstring de la función original
    def wrapper(*args, **kwargs):
        # Creamos una clave única basada en los argumentos
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

@cache_decorator
def expensive_computation(x: int, y: int) -> int:
    """Simula una operación costosa."""
    # Imagina que esto toma 5 segundos en ejecutarse
    return x * y


# ==========================================
# 3. ADAPTER (Patrón Estructural)
# ==========================================
# Objetivo: Hacer que una clase externa incompatible funcione con nuestra interfaz.

# Interfaz que nuestra aplicación espera usar
class NotificationService(ABC):
    @abstractmethod
    def send(self, message: str, recipient: str) -> bool:
        pass

# Proveedor externo (Tiene una interfaz completamente distinta que no podemos modificar)
class LegacySMSProvider:
    def push_text_message(self, phone_number: str, text: str) -> str:
        # Retorna "200 OK" si funciona, "500 ERR" si falla
        if phone_number and text:
            return "200 OK"
        return "500 ERR"

# El Adaptador: Implementa NUESTRA interfaz, pero por dentro llama al proveedor externo
class LegacySMSAdapter(NotificationService):
    def __init__(self, legacy_provider: LegacySMSProvider):
        self._provider = legacy_provider

    def send(self, message: str, recipient: str) -> bool:
        response = self._provider.push_text_message(
            phone_number=recipient, 
            text=message
        )
        return response == "200 OK"