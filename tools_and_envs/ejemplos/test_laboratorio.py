import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.modulo_http_apis.cliente_httpx import ClienteRobusto
from src.modulo_http_apis.streaming_descarga import descargar_archivo_streaming

def main():
    print("=" * 60)
    print("🚀 LABORATORIO HTTP - Smocker")
    print("=" * 60)
    
    cliente = ClienteRobusto(base_url="http://localhost:9080", timeout=5)
    
    # Test 1: GET exitoso
    print("\n1️⃣ TEST: GET exitoso")
    print("-" * 60)
    try:
        datos = cliente.get_con_reintentos("/datos")
        print(f"✅ {datos}")
    except Exception as e:
        print(f"❌ {e}")
    
    # Test 2: Timeout
    print("\n2️⃣ TEST: Timeout (endpoint lento)")
    print("-" * 60)
    try:
        datos = cliente.get_con_reintentos("/lento")
        print(f"✅ {datos}")
    except Exception as e:
        print(f"⏱️ Timeout capturado correctamente")
    
    # Test 3: Error 500
    print("\n3️⃣ TEST: Manejo de error 500")
    print("-" * 60)
    try:
        datos = cliente.get_con_reintentos("/error")
        print(f"✅ {datos}")
    except Exception as e:
        print(f"❌ Error capturado correctamente")
    
    # Test 4: Streaming
    print("\n4️⃣ TEST: Descarga por streaming")
    print("-" * 60)
    try:
        descargar_archivo_streaming(
            "http://localhost:9080/archivo",
            "descarga_test.txt"
        )
    except Exception as e:
        print(f"❌ {e}")
    
    print("\n" + "=" * 60)
    print("✅ Laboratorio completado")

if __name__ == "__main__":
    main()