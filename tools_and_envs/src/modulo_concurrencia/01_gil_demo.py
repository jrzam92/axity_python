"""
Demostración del GIL (Global Interpreter Lock)

El GIL impide que múltiples threads ejecuten bytecode Python simultáneamente.
Por eso, threading NO mejora el rendimiento en tareas CPU-bound.
"""
import threading
import time
from src.modulo_concurrencia.utils.timer import timer

def tarea_cpu_bound(n: int):
    """Tarea que consume CPU"""
    total = 0
    for i in range(n):
        total += i ** 2
    return total

@timer
def con_threading(n: int, num_threads: int = 4):
    """Ejecuta tarea CPU-bound con threads"""
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=tarea_cpu_bound, args=(n // num_threads,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

@timer
def sin_threading(n: int):
    """Ejecuta tarea CPU-bound secuencialmente"""
    tarea_cpu_bound(n)

if __name__ == "__main__":
    print("=" * 60)
    print("🔒 DEMOSTRACIÓN DEL GIL")
    print("=" * 60)
    
    N = 10_000_000
    
    print("\n1️⃣ Sin threading (secuencial):")
    sin_threading(N)
    
    print("\n2️⃣ Con threading (4 threads):")
    con_threading(N, 4)
    
    print("\n❌ Resultado: Threading NO mejora (o empeora) el rendimiento")
    print("   en tareas CPU-bound debido al GIL.")