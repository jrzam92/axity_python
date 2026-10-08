"""
LABORATORIO: Procesamiento paralelo con ProcessPoolExecutor

Objetivo: Demostrar ventajas de multiprocessing en CPU-bound
"""
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
import time

def es_primo(n: int) -> bool:
    """Verifica si un número es primo"""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def contar_primos_rango(start: int, end: int) -> int:
    """Cuenta primos en un rango"""
    return sum(1 for n in range(start, end) if es_primo(n))

def procesar_secuencial(ranges: list):
    """Procesa rangos secuencialmente"""
    start = time.perf_counter()
    results = [contar_primos_rango(s, e) for s, e in ranges]
    elapsed = time.perf_counter() - start
    print(f"⏱️  Secuencial: {elapsed:.2f}s | Total primos: {sum(results)}")
    return results

def procesar_paralelo(ranges: list, workers: int):
    """Procesa rangos en paralelo"""
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=workers) as executor:
        results = list(executor.starmap(contar_primos_rango, ranges))
    elapsed = time.perf_counter() - start
    print(f"⏱️  Paralelo ({workers} workers): {elapsed:.2f}s | Total primos: {sum(results)}")
    return results

if __name__ == "__main__":
    print("=" * 70)
    print("⚙️  LABORATORIO: Procesamiento Paralelo (CPU-bound)")
    print("=" * 70)
    print(f"\n💻 CPUs disponibles: {cpu_count()}\n")
    
    # Dividir 1 millón de números en 8 rangos
    TOTAL = 1_000_000
    NUM_RANGES = 8
    CHUNK_SIZE = TOTAL // NUM_RANGES
    RANGES = [(i * CHUNK_SIZE, (i + 1) * CHUNK_SIZE) for i in range(NUM_RANGES)]
    
    print(f"🔢 Contando primos de 1 a {TOTAL:,} (dividido en {NUM_RANGES} rangos)\n")
    
    print("1️⃣ Procesamiento secuencial:")
    procesar_secuencial(RANGES)
    
    print("\n2️⃣ Procesamiento paralelo (2 workers):")
    procesar_paralelo(RANGES, workers=2)
    
    print("\n3️⃣ Procesamiento paralelo (4 workers):")
    procesar_paralelo(RANGES, workers=4)
    
    if cpu_count() >= 8:
        print("\n4️⃣ Procesamiento paralelo (8 workers):")
        procesar_paralelo(RANGES, workers=8)