import uuid
from dataclasses import dataclass, field

# Agregamos Union, Literal y Dict de typing (Contenido clave del módulo)
from typing import Dict, List, Literal, Union

# Definimos un tipo estricto usando Literal
EstadoOrden = Literal["PENDIENTE", "PAGADA", "EN_ENVIO", "ENTREGADA"]


@dataclass
class Order:
    customer_name: str
    items: List[float]
    discount: float = 0.0
    # Usamos Literal aquí para que solo acepte esos 4 estados
    status: EstadoOrden = "PENDIENTE"
    # Usamos Union por si el metadata puede ser un diccionario o simplemente None
    metadata: Union[Dict[str, str], None] = None
    order_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    @property
    def total(self) -> float:
        subtotal = sum(self.items)
        return subtotal - (subtotal * self.discount)

    def __str__(self) -> str:  # Anotamos que retorna un string
        return f"Orden [{self.order_id}] | Estado: {self.status} | Total: ${self.total:.2f}"
