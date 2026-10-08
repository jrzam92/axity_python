from dataclasses import dataclass

@dataclass
class OrderCreated:
    """Evento de dominio que indica que se creó una orden."""
    order_id: str
    amount: float