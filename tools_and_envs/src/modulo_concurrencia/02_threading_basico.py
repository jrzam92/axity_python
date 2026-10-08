"""
Threading para tareas I/O-bound

Threading es útil cuando el programa pasa tiempo esperando (I/O).
"""
import threading
import time
from src.modulo_concurrencia.utils.timer import timer

def descarga_simulada(file_id: int):
    """Simula descarga de archivo (I/O-bound)"""
    print(f"📥 Descargando archivo {file_id}...")
    time.sleep(2)  # Simula espera de red
    print(f"✅ Archivo {file_id} descargado")
    return f"file_{file_id}.txt"

@timer
def descargar_secuencial(num_files: int):
    """Descarga archivos secuencialmente"""
    for i in range(num_files):
        descarga_simulada(i)

@timer
def descargar_con_threads(num_files: int):
    """Descarga archivos con threads"""
    threads = []
    for i in range(num_files):
        thread = threading.Thread(target=descarga_simulada, args=(i,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    print("=" * 60)
    print("🧵 THREADING PARA I/O-BOUND")
    print("=" * 60)
    
    NUM_FILES = 5
    
    print("\n1️⃣ Descarga secuencial:")
    descargar_secuencial(NUM_FILES)
    
    print("\n2️⃣ Descarga con threads:")
    descargar_con_threads(NUM_FILES)
    
    print("\n✅ Resultado: Threading mejora significativamente tareas I/O-bound")