"""
Multiprocessing para tareas CPU-bound

Bypasea el GIL usando procesos separados.
"""
from multiprocessing import Pool, cpu_count
from src.modulo_concurrencia.utils.timer import timer
from src.modulo_concurrencia.utils.cpu_tasks import contar_primos, fibonacci_recursivo

@timer
def sin_multiprocessing(ranges: list):
    """Cuenta primos secuencialmente"""
    results = []
    for start, end in ranges:
        result = contar_primos(start, end)
        results.append(result)
    return results

@timer
def con_multiprocessing(ranges: list, num_workers: int = None):
    """Cuenta primos con multiprocessing"""
    if num_workers is None:
        num_workers = cpu_count()
    
    with Pool(processes=num_workers) as pool:
        results = pool.starmap(contar_primos, ranges)
    
    return results

if __name__ == "__main__":
    print("=" * 60)
    print("⚙️  MULTIPROCESSING PARA CPU-BOUND")
    print("=" * 60)
    
    print(f"\n💻 CPUs disponibles: {cpu_count()}\n")
    
    # Rangos para contar primos
    RANGES = [
        (1, 250000),
        (250000, 500000),
        (500000, 750000),
        (750000, 1000000),
    ]
    
    print("1️⃣ Sin multiprocessing (secuencial):")
    results1 = sin_multiprocessing(RANGES)
    print(f"   Total de primos: {sum(results1)}")
    
    print("\n2️⃣ Con multiprocessing:")
    results2 = con_multiprocessing(RANGES, num_workers=4)
    print(f"   Total de primos: {sum(results2)}")