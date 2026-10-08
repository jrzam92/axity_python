"""
LABORATORIO: Fetcher concurrente con httpx.AsyncClient

Objetivo: Comparar rendimiento de descarga síncrona vs asíncrona
"""
import asyncio
import httpx
import time

# URLs de prueba (JSONPlaceholder)
URLS = [f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, 51)]

def fetch_sync(urls: list):
    """Descarga síncrona con httpx"""
    start = time.perf_counter()
    
    with httpx.Client(timeout=10.0) as client:
        results = []
        for url in urls:
            try:
                response = client.get(url)
                results.append(response.json())
            except Exception as e:
                print(f"❌ Error: {e}")
        
    elapsed = time.perf_counter() - start
    print(f"⏱️  Síncrono: {elapsed:.2f}s | {len(results)} descargas")
    return results

async def fetch_async(urls: list, max_concurrent: int = 10):
    """Descarga asíncrona con semáforo"""
    start = time.perf_counter()
    semaforo = asyncio.Semaphore(max_concurrent)
    
    async def fetch_one(client: httpx.AsyncClient, url: str):
        async with semaforo:
            try:
                response = await client.get(url)
                return response.json()
            except Exception as e:
                print(f"❌ Error: {e}")
                return None
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [fetch_one(client, url) for url in urls]
        results = await asyncio.gather(*tasks)
    
    elapsed = time.perf_counter() - start
    print(f"⏱️  Asíncrono: {elapsed:.2f}s | {len([r for r in results if r])} descargas")
    return results

if __name__ == "__main__":
    print("=" * 70)
    print("🚀 LABORATORIO: Fetcher Concurrente")
    print("=" * 70)
    print(f"\n📡 Descargando {len(URLS)} URLs...\n")
    
    print("1️⃣ Modo síncrono:")
    fetch_sync(URLS)
    
    print("\n2️⃣ Modo asíncrono (máx. 10 concurrentes):")
    asyncio.run(fetch_async(URLS, max_concurrent=10))
    
    print("\n3️⃣ Modo asíncrono (máx. 20 concurrentes):")
    asyncio.run(fetch_async(URLS, max_concurrent=20))