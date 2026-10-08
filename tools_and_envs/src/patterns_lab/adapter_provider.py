# src/patterns_lab/adapter_provider.py

# 1. Interfaz que nuestro sistema espera (Target)
class PaymentProcessor:
    def pay(self, amount: float) -> str:
        raise NotImplementedError

# 2. Proveedor externo con interfaz incompatible (Adaptee)
class StripeExternalAPI:
    def make_payment(self, total: float, currency: str) -> str:
        return f"Pago procesado en Stripe: {total} {currency}"

# 3. El Adaptador
class StripeAdapter(PaymentProcessor):
    def __init__(self, stripe_api: StripeExternalAPI):
        self.stripe_api = stripe_api

    def pay(self, amount: float) -> str:
        # Adaptamos nuestra entrada a lo que pide Stripe
        return self.stripe_api.make_payment(total=amount, currency="USD")