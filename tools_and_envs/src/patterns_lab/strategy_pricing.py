# src/patterns_lab/strategy_pricing.py
from abc import ABC, abstractmethod
from dataclasses import dataclass

# Interfaz para nuestras estrategias
class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, base_price: float) -> float:
        pass

# Estrategia 1: Precio normal
class NormalPricing(PricingStrategy):
    def calculate(self, base_price: float) -> float:
        return base_price

# Estrategia 2: Descuento del 20%
class DiscountPricing(PricingStrategy):
    def calculate(self, base_price: float) -> float:
        return base_price * 0.80

# El "Contexto" que usa la estrategia. Usamos un dataclass.
@dataclass
class Order:
    base_price: float
    strategy: PricingStrategy

    def checkout(self) -> float:
        return self.strategy.calculate(self.base_price)