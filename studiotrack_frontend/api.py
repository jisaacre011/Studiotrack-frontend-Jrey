# Cliente HTTP hacia el backend FastAPI.
# La URL base sale de una variable de entorno para que en produccion
# apunte al backend en Render sin tocar codigo.
import os
import httpx

# En local apunta al backend en el puerto 8001.
# En produccion se define API_URL en las variables de entorno de Render.
API_URL = os.getenv("API_URL", "http://localhost:8001")


async def get_estudios() -> list[dict]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_URL}/estudios", timeout=10)
        resp.raise_for_status()
        return resp.json()


async def get_estudio(estudio_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_URL}/estudios/{estudio_id}", timeout=10)
        resp.raise_for_status()
        return resp.json()


async def crear_reserva(data: dict) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_URL}/reservas", json=data, timeout=10)
        resp.raise_for_status()
        return resp.json()