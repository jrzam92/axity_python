import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

class ClienteRobusto:
    def __init__(self, base_url: str, timeout: int = 10):
        self.client = httpx.Client(
            base_url=base_url,
            timeout=timeout,
            http2=True
        )
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def get_con_reintentos(self, endpoint: str):
        """GET con reintentos automáticos"""
        try:
            print(f"🔄 Intentando GET {endpoint}...")
            response = self.client.get(endpoint)
            response.raise_for_status()
            print(f"✅ Respuesta exitosa: {response.status_code}")
            return response.json()
        except httpx.TimeoutException as e:
            print(f"⏱️ Timeout en {endpoint}: {e}")
            raise
        except httpx.HTTPStatusError as e:
            print(f"❌ Error HTTP {e.response.status_code}")
            raise
    
    def __del__(self):
        self.client.close()