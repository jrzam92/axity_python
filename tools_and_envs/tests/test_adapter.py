from patterns_lab.adapter_provider import StripeExternalAPI, StripeAdapter

def test_stripe_adapter():
    external_api = StripeExternalAPI()
    adapter = StripeAdapter(external_api)
    
    result = adapter.pay(50.0)
    
    # Verificamos que el adaptador transformó la petición correctamente
    assert result == "Pago procesado en Stripe: 50.0 USD"