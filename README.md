# StudioTrack — Frontend

Interfaz web de StudioTrack, una plataforma para reservar estudios de grabación
y salas de ensayo. Hecha con Reflex (Python), conectada a una API FastAPI.

El proyecto tiene dos repos:
- Este repo — interfaz en Reflex
- [studiotrack-backend](https://github.com/jisaacre011/Studiotrack-backend-Jrey) — API FastAPI

Demo: https://studiotrack-frontend-jrey.onrender.com

## Tecnologías

Python 3, Reflex, httpx, Render.

## Cómo correrlo local

El backend tiene que estar corriendo primero en el puerto 8001.

1. Clonar el repo y entrar a la carpeta
2. Crear el entorno virtual: `python -m venv venv`
3. Activarlo: `.\venv\Scripts\activate`
4. Instalar dependencias: `python -m pip install -r requirements.txt`
5. Inicializar Reflex: `reflex init`
6. Correr: `reflex run`

Frontend en http://localhost:3000

## Estructura
studiotrack_frontend/
studiotrack_frontend.py  # app principal y rutas
theme.py                 # colores y tipografía
state.py                 # estado de la app
api.py                   # conexión al backend
pages/
index.py     # inicio: catálogo y contacto
sala.py      # detalle de sala
reservar.py  # formulario de reserva
components/
navbar.py    # navegación
sala_card.py # card de sala


## Créditos

Desarrollado por Juan Isaac.
