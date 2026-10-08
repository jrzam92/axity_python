from pydantic import BaseModel

class CreateOrderRequest(BaseModel):
    item_name: str
    quantity: int

class CreateOrderResponse(BaseModel):
    order_id: str
    status: str