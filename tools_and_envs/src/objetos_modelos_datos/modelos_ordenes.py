import uuid
from dataclasses import dataclass, field
from typing import List

from pydantic import BaseModel, Field, ValidationError, field_validator


# ==========================================
# 1. ENTIDAD DE DOMINIO (Dataclass)
# Aquí viven las reglas de negocio, los cálculos y comportamientos puros.
# ==========================================
@dataclass
class Order:
    customer_name: str
    items: List[float]  # Lista de precios de los artículos
    discount: float = 0.0
    # Generamos un ID único automáticamente al crear la orden
    order_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    # --- Cálculos derivados ---
    @property
    def total(self) -> float:
        """Calcula el total aplicando el descuento."""
        subtotal = sum(self.items)
        return subtotal - (subtotal * self.discount)

    # --- Dunder Methods (Métodos Mágicos) ---
    def __str__(self):
        """Define cómo se imprime la orden de forma legible (comportamiento)."""
        return f"Orden [{self.order_id}] | Cliente: {self.customer_name} | Total: ${self.total:.2f}"

    def __eq__(self, other):
        """Permite comparar si dos órdenes valen lo mismo usando '=='."""
        if not isinstance(other, Order):
            return NotImplemented
        return self.total == other.total

    def __lt__(self, other):
        """Permite saber si esta orden es menor a otra usando '<'."""
        if not isinstance(other, Order):
            return NotImplemented
        return self.total < other.total


# ==========================================
# 2. MODELOS DE ENTRADA Y SALIDA (Pydantic)
# Estos son los "cadeneros" (guardias) de tu API. Validan todo lo que entra y sale.
# ==========================================
class OrderIn(BaseModel):
    """Modelo para validar los datos que el usuario nos manda (Ej. un JSON)."""

    customer_name: str = Field(..., min_length=3, max_length=50)
    items: List[float] = Field(..., min_items=1)
    discount: float = Field(default=0.0, ge=0.0, le=1.0)  # Descuento de 0% a 100%

    @field_validator("items")
    def check_precios_positivos(cls, value):
        """Validación personalizada: ningún precio puede ser negativo o gratis."""
        if any(precio <= 0 for precio in value):
            raise ValueError("Todos los precios de los items deben ser mayores a 0")
        return value

    def to_entity(self) -> Order:
        """Convierte este modelo validado a nuestra Entidad de negocio."""
        return Order(
            customer_name=self.customer_name, items=self.items, discount=self.discount
        )


class OrderOut(BaseModel):
    """Modelo para formatear los datos que le devolveremos al usuario."""

    order_id: str
    customer_name: str
    total_pagar: float

    @classmethod
    def from_entity(cls, order: Order):
        """Construye la respuesta a partir de nuestra Entidad de negocio."""
        return cls(
            order_id=order.order_id,
            customer_name=order.customer_name,
            total_pagar=order.total,
        )


# ==========================================
# 3. PRUEBA DEL LABORATORIO
# ==========================================
if __name__ == "__main__":
    print("--- 🛒 SIMULACIÓN DE FLUJO DE ÓRDENES ---\n")

    # Simulamos un JSON que llega de internet (API)
    payload_json = {
        "customer_name": "Ana",
        "items": [150.0, 50.0],  # Subtotal 200
        "discount": 0.10,  # 10% de descuento
    }

    try:
        # 1. Pydantic valida la entrada
        print("📥 1. Validando datos de entrada (OrderIn)...")
        order_in = OrderIn.model_validate(payload_json)
        print(f"Datos válidos: {order_in.model_dump()}")

        # 2. Conversión a Entidad (Dataclass)
        print("\n⚙️ 2. Convirtiendo a Entidad y calculando derivados...")
        entidad_order1 = order_in.to_entity()
        print(entidad_order1)  # Aquí entra en acción el dunder method __str__

        # 3. Probando comparaciones (Dunder methods)
        print("\n⚖️ 3. Probando comparaciones (Dunder methods)...")
        entidad_order2 = Order(customer_name="Juan", items=[500.0])  # Total 500
        print(
            f"¿La orden de Ana es más barata que la de Juan?: {entidad_order1 < entidad_order2}"
        )

        # 4. Preparando la salida con Pydantic
        print("\n📤 4. Preparando la respuesta para el usuario (OrderOut)...")
        order_out = OrderOut.from_entity(entidad_order1)
        print(f"Respuesta final (JSON ready): {order_out.model_dump_json(indent=2)}")

    except ValidationError as e:
        print(f"❌ Error de validación: {e.errors()}")
