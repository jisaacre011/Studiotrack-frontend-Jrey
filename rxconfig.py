# Configuracion de Reflex para desarrollo y produccion.
import os
import reflex as rx

# En produccion, Render define estas variables. En local usan los defaults.
config = rx.Config(
    app_name="studiotrack_frontend",
    # URL publica donde corre el backend de Reflex (el propio, no FastAPI).
    # En Render sera la URL del servicio frontend.
    api_url=os.getenv("API_URL_REFLEX", "http://localhost:8000"),
    # Reflex sirve en el puerto que Render inyecte.
    frontend_port=int(os.getenv("PORT", "3000")),
)