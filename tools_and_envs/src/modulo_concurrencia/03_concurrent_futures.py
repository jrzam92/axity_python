"""
concurrent.futures: ThreadPoolExecutor y ProcessPoolExecutor

API de alto nivel para threading y multiprocessing.
"""
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import time
from src.modulo_concurrencia.utils.timer import timer
from src.modulo_concurrencia.utils.cpu_tasks import contar_primos

def tarea_io(task_id: int, delay: float = 1.0):
    """Simula tarea I/O"""
    time.sleep(delay)
    return f"Tarea {task_id} completada"

@timer
def con_threadpool(num_tasks: int, max_workers: int = 4):
    """Ejecuta tareas I/O con ThreadPoolExecutor"""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(tarea_io, i) for i in range(num_tasks)]
        
        for future in as_completed(futures):
            result = future.result()
            print(f"  ✅ {result}")

@timer
def con_processpool(ranges: list, max_workers: int = 4):
    """Ejecuta tareas CPU-bound con ProcessPoolExecutor"""
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(contar_primos, start, end): (start, end) 
                   for start, end in ranges}
        
        for future in as_completed(futures):
            rango = futures[future]
            result = future.result()
            print(f"  ✅ Primos en rango {rango}: {result}")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 CONCURRENT.FUTURES")
    print("=" * 60)
    
    print("\n1️⃣ ThreadPoolExecutor (I/O-bound):")
    con_threadpool(10, max_workers=5)
    
    print("\n2️⃣ ProcessPoolExecutor (CPU-bound):")
    ranges = [(1, 100000), (100000, 200000), (200000, 300000), (300000, 400000)]
    con_processpool(ranges, max_workers=4)