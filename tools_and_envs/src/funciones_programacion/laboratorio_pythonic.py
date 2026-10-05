import random
import time
from contextlib import contextmanager
from functools import wraps


# ==========================================
# 1. CONTEXT MANAGER: Temporizador
# ==========================================
# Usamos un generador y un decorador nativo para crear un context manager
@contextmanager
def temporizador():
    """Mide el tiempo de ejecución de un bloque de código."""
    inicio = time.time()
    try:
        # Aquí es donde cede el control al código que está dentro del "with"
        yield
    finally:
        fin = time.time()
        print(f"⏱️ Tiempo total de ejecución: {fin - inicio:.4f} segundos\n")


# ==========================================
# 2. DECORADOR: Reintentos con Backoff
# ==========================================
# Un "backoff" significa que si falla, espera 1 segundo, luego 2, luego 4...
# Usamos closures y *args / **kwargs para que acepte cualquier función.
def reintentar(max_intentos=3, backoff_factor=2):
    def decorador(func):
        @wraps(func)  # Esto conserva el nombre original de la función
        def wrapper(*args, **kwargs):
            espera = 1
            for intento in range(1, max_intentos + 1):
                try:
                    # Intentamos ejecutar la función original
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"⚠️ Intento {intento}/{max_intentos} falló: {e}")
                    if intento == max_intentos:
                        print("❌ Se agotaron los intentos.")
                        raise e  # Si es el último intento, lanzamos el error

                    print(f"⏳ Esperando {espera} segundos antes de reintentar...")
                    time.sleep(espera)
                    espera *= backoff_factor  # Aumentamos el tiempo de espera

        return wrapper

    return decorador


# ==========================================
# 3. GENERADOR: Procesamiento por lotes (Batches)
# ==========================================
# Usamos 'yield' para no cargar toda la memoria de golpe (lazy evaluation)
def generador_lotes(datos, tamaño_lote):
    """Toma una lista y la devuelve en pequeños pedazos."""
    for i in range(0, len(datos), tamaño_lote):
        # Hacemos "slicing" de la lista y lo devolvemos pausando la función
        yield datos[i : i + tamaño_lote]


# ==========================================
# PRUEBA DEL LABORATORIO
# ==========================================


# Aplicamos nuestro decorador a una función que simula conectarse a una API
@reintentar(max_intentos=4, backoff_factor=2)
def conectar_api_inestable():
    """Simula una función que a veces falla (como una petición HTTP real)."""
    # 70% de probabilidad de fallar
    if random.random() < 0.70:
        raise ConnectionError("Se cayó la red 😭")
    return "✅ ¡Conexión exitosa a la API!"


if __name__ == "__main__":
    print("--- INICIANDO LABORATORIO PYTHONIC ---\n")

    # A. Probamos el Generador y el Context Manager juntos
    datos_completos = list(range(1, 101))  # Una lista del 1 al 100

    print("📦 Procesando datos en lotes...")
    # Usamos nuestro Context Manager con la palabra 'with'
    with temporizador():
        for lote in generador_lotes(datos_completos, tamaño_lote=25):
            print(f"Procesando lote: {lote}")
            time.sleep(0.5)  # Simulamos que tarda un poco en procesar cada lote

    # B. Probamos el Decorador de reintentos
    print("🔌 Probando conexión a sistema inestable...")
    try:
        resultado = conectar_api_inestable()
        print(resultado)
    except ConnectionError:
        print("No se pudo conectar después de todos los intentos.")
