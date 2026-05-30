# App principal de StudioTrack.
# Registra las 3 paginas con sus rutas y carga las fuentes de Google.
import reflex as rx

from studiotrack_frontend.theme import COLORS
from studiotrack_frontend.pages.index import index
from studiotrack_frontend.pages.sala import sala
from studiotrack_frontend.pages.reservar import reservar

app = rx.App(
    style={"font_family": "'IBM Plex Mono', monospace"},
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap",
    ],
)

# Registro de rutas.
app.add_page(index, route="/", title="StudioTrack")
app.add_page(sala, route="/sala/[id]", title="Detalle de sala")
app.add_page(reservar, route="/reservar", title="Reservar")