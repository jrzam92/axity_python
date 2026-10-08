from dataclasses import dataclass, field
from typing import List, Any
from .events import OrderCreated

@dataclass
class Order:  # <--- Verifica que el nombre sea exactamente este
    id: str
    amount: float
    events: List[Any] = field(default_factory=list)

    def create(self):
        self.events.append(OrderCreated(order_id=self.id, amount=self.amount))