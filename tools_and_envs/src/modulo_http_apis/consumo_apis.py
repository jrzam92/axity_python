# modulo_http_apis/consumo_apis.py
import requests
import httpx
import asyncio
import aiohttp

# 1. requests (síncrono, simple)
def con_requests(url):
    response = requests.get(url, timeout=5)
    return response.json()

# 2. httpx (síncrono/asíncrono + HTTP/2)
def con_httpx(url):
    with httpx.Client(http2=True) as client:
        response = client.get(url)
        return response.json()

# 3. aiohttp (asíncrono puro)
async def con_aiohttp(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()