from dataclasses import dataclass
import uuid

@dataclass
class Order:
    """Entidad de dominio puro."""
    item_name: str
    quantity: int
    id: str = None

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())