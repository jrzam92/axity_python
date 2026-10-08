"""
Comparación de todos los modelos de concurrencia
"""
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from modulo_concurrencia.utils.timer import timer, async_timer
from modulo_concurrencia.utils.cpu_tasks import contar_primos

# Tarea I/O simulada
def io_task(task_id: int):
    time.sleep(0.5)
    return task_id

# Tarea CPU-bound
def cpu_task(n: int):
    return contar_primos(1, n)

@timer
def io_secuencial(num_tasks: int):
    """I/O secuencial"""
    return [io_task(i) for i in range(num_tasks)]

@timer
def io_threading(num_tasks: int):
    """I/O con ThreadPoolExecutor"""
    with ThreadPoolExecutor(max_workers=10) as executor:
        return list(executor.map(io_task, range(num_tasks)))

@async_timer
async def io_asyncio(num_tasks: int):
    """I/O con asyncio"""
    async def async_io_task(task_id: int):
        await asyncio.sleep(0.5)
        return task_id
    
    tasks = [async_io_task(i) for i in range(num_tasks)]
    return await asyncio.gather(*tasks)

@timer
def cpu_secuencial(ranges: list):
    """CPU-bound secuencial"""
    return [contar_primos(start, end) for start, end in ranges]

@timer
def cpu_multiprocessing(ranges: list):
    """CPU-bound con ProcessPoolExecutor"""
    with ProcessPoolExecutor(max_workers=4) as executor:
        # Opción 1: Usando submit()
        futures = [executor.submit(contar_primos, start, end) for start, end in ranges]
        return [future.result() for future in futures]

if __name__ == "__main__":
    print("=" * 70)
    print("📊 COMPARACIÓN DE MODELOS DE CONCURRENCIA")
    print("=" * 70)
    
    # Test I/O-bound
    print("\n🌐 TAREAS I/O-BOUND (20 tareas de 0.5s cada una):")
    print("-" * 70)
    io_secuencial(20)
    io_threading(20)
    asyncio.run(io_asyncio(20))
    
    # Test CPU-bound
    print("\n⚙️  TAREAS CPU-BOUND (contar primos en 4 rangos):")
    print("-" * 70)
    RANGES = [(1, 100000), (100000, 200000), (200000, 300000), (300000, 400000)]
    cpu_secuencial(RANGES)
    cpu_multiprocessing(RANGES)
    
    print("\n" + "=" * 70)
    print("📌 CONCLUSIONES:")
    print("  • I/O-bound: asyncio > threading >> secuencial")
    print("  • CPU-bound: multiprocessing >> secuencial > threading (GIL)")
    print("=" * 70)