"""
Asyncio: Event loop y async/await

Modelo de concurrencia cooperativa ideal para I/O-bound.
"""
import asyncio
from src.modulo_concurrencia.utils.timer import async_timer

async def tarea_async(task_id: int, delay: float = 1.0):
    """Tarea asíncrona"""
    print(f"  🔄 Tarea {task_id} iniciada")
    await asyncio.sleep(delay)
    print(f"  ✅ Tarea {task_id} completada")
    return f"Resultado de tarea {task_id}"

@async_timer
async def ejecutar_secuencial(num_tasks: int):
    """Ejecuta tareas secuencialmente (await uno por uno)"""
    for i in range(num_tasks):
        await tarea_async(i)

@async_timer
async def ejecutar_concurrente(num_tasks: int):
    """Ejecuta tareas concurrentemente (gather)"""
    tasks = [tarea_async(i) for i in range(num_tasks)]
    results = await asyncio.gather(*tasks)
    return results

@async_timer
async def con_semaforo(num_tasks: int, max_concurrent: int = 3):
    """Limita concurrencia con semáforo"""
    semaforo = asyncio.Semaphore(max_concurrent)
    
    async def tarea_limitada(task_id: int):
        async with semaforo:
            return await tarea_async(task_id)
    
    tasks = [tarea_limitada(i) for i in range(num_tasks)]
    return await asyncio.gather(*tasks)

if __name__ == "__main__":
    print("=" * 60)
    print("⚡ ASYNCIO: ASYNC/AWAIT")
    print("=" * 60)
    
    NUM_TASKS = 10
    
    print("\n1️⃣ Ejecución secuencial:")
    asyncio.run(ejecutar_secuencial(NUM_TASKS))
    
    print("\n2️⃣ Ejecución concurrente (gather):")
    asyncio.run(ejecutar_concurrente(NUM_TASKS))
    
    print("\n3️⃣ Concurrencia limitada (semáforo = 3):")
    asyncio.run(con_semaforo(NUM_TASKS, max_concurrent=3))