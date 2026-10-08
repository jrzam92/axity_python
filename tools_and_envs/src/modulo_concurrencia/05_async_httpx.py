"""
Cliente HTTP asíncrono con httpx.AsyncClient

Fetch múltiples URLs concurrentemente.
"""
import asyncio
import httpx
from src.modulo_concurrencia.utils.timer import async_timer

URLS = [
    "https://api.github.com/users/octocat",
    "https://api.github.com/users/torvalds",
    "https://api.github.com/users/gvanrossum",
    "https://api.github.com/users/mitsuhiko",
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/2",
    "https://jsonplaceholder.typicode.com/posts/3",
]

async def fetch_url(client: httpx.AsyncClient, url: str):
    """Descarga una URL"""
    try:
        response = await client.get(url, timeout=10.0)
        response.raise_for_status()
        print(f"  ✅ {url}: {response.status_code}")
        return response.json()
    except Exception as e:
        print(f"  ❌ {url}: {e}")
        return None

@async_timer
async def fetch_secuencial(urls: list):
    """Descarga URLs secuencialmente"""
    async with httpx.AsyncClient() as client:
        results = []
        for url in urls:
            result = await fetch_url(client, url)
            results.append(result)
        return results

@async_timer
async def fetch_concurrente(urls: list):
    """Descarga URLs concurrentemente"""
    async with httpx.AsyncClient() as client:
        tasks = [fetch_url(client, url) for url in urls]
        return await asyncio.gather(*tasks)

@async_timer
async def fetch_con_semaforo(urls: list, max_concurrent: int = 3):
    """Descarga URLs con límite de concurrencia"""
    semaforo = asyncio.Semaphore(max_concurrent)
    
    async def fetch_limitado(client: httpx.AsyncClient, url: str):
        async with semaforo:
            return await fetch_url(client, url)
    
    async with httpx.AsyncClient() as client:
        tasks = [fetch_limitado(client, url) for url in urls]
        return await asyncio.gather(*tasks)

if __name__ == "__main__":
    print("=" * 60)
    print("🌐 HTTPX ASYNC CLIENT")
    print("=" * 60)
    
    print(f"\n📡 Descargando {len(URLS)} URLs...\n")
    
    print("1️⃣ Secuencial:")
    asyncio.run(fetch_secuencial(URLS))
    
    print("\n2️⃣ Concurrente (sin límite):")
    asyncio.run(fetch_concurrente(URLS))
    
    print("\n3️⃣ Concurrente (máximo 3 simultáneas):")
    asyncio.run(fetch_con_semaforo(URLS, max_concurrent=3))