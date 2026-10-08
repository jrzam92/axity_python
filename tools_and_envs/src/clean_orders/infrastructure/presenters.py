from src.clean_orders.application.interfaces import Presenter

class APIPresenter(Presenter):
    def present_success(self, order_id: str) -> dict:
        # Transforma el resultado en un JSON/Dict limpio para la respuesta
        return {
            "status": "success",
            "message": "Orden creada correctamente",
            "data": {"order_id": order_id}
        }