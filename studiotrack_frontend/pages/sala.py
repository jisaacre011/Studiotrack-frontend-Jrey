# Pagina de detalle de una sala: galeria, descripcion tecnica, equipos y reglas.
import reflex as rx

from studiotrack_frontend.theme import COLORS, FONT_DISPLAY, FONT_BODY, CARD_STYLE
from studiotrack_frontend.state import State
from studiotrack_frontend.components.navbar import navbar


def equipo_item(equipo: dict) -> rx.Component:
    return rx.box(
        rx.text(equipo["nombre"], font_family=FONT_BODY, color=COLORS["text_primary"], font_weight="600"),
        rx.text(equipo["descripcion"], font_family=FONT_BODY, color=COLORS["text_muted"], font_size="0.85em"),
        rx.text(f"Cantidad: {equipo['cantidad']}", font_family=FONT_BODY, color=COLORS["accent_teal"], font_size="0.8em"),
        padding="0.8em",
        border=f"1px solid {COLORS['border']}",
        border_radius="10px",
        width="100%",
    )


def sala() -> rx.Component:
    return rx.box(
        navbar(),
        rx.cond(
            State.sala_actual,
            rx.vstack(
                rx.image(
                    src=State.sala_actual["imagen_url"],
                    width="100%",
                    height="320px",
                    object_fit="cover",
                    border_radius="16px",
                ),
                rx.heading(
                    State.sala_actual["nombre"],
                    font_family=FONT_DISPLAY,
                    color=COLORS["text_primary"],
                    size="8",
                ),
                rx.text(
                    State.sala_actual["descripcion"],
                    font_family=FONT_BODY,
                    color=COLORS["text_muted"],
                ),
                rx.hstack(
                    rx.text(
                        f"${State.sala_actual['precio_hora']}/hora",
                        font_family=FONT_BODY,
                        color=COLORS["accent_amber"],
                        font_weight="600",
                        font_size="1.2em",
                    ),
                    rx.text(
                        f"Capacidad: {State.sala_actual['capacidad']}",
                        font_family=FONT_BODY,
                        color=COLORS["text_muted"],
                    ),
                    spacing="5",
                ),
                # Equipo tecnico.
                rx.heading("Equipo tecnico", font_family=FONT_DISPLAY, color=COLORS["text_primary"], size="5"),
                rx.vstack(
                    rx.foreach(State.equipos, equipo_item),
                    width="100%",
                    spacing="2",
                ),
                # Reglas de sesion (contenido estatico segun spec).
                rx.box(
                    rx.heading("Reglas de sesion", font_family=FONT_DISPLAY, color=COLORS["text_primary"], size="4"),
                    rx.text(
                        "Horario: 9:00 a 22:00. Cancelacion gratuita hasta 24h antes. "
                        "Llegar 10 min antes de la sesion.",
                        font_family=FONT_BODY,
                        color=COLORS["text_muted"],
                    ),
                    **CARD_STYLE,
                    width="100%",
                ),
                rx.link(
                    rx.button(
                        "Reservar esta sala",
                        background=COLORS["accent_purple"],
                        color="white",
                        border_radius="10px",
                        padding="0.9em 2em",
                        font_family=FONT_BODY,
                        font_weight="600",
                        cursor="pointer",
                    ),
                    href="/reservar",
                ),
                spacing="4",
                padding="2em",
                max_width="800px",
                margin="0 auto",
            ),
            rx.text("Cargando sala...", color=COLORS["text_muted"], padding="2em"),
        ),
        on_mount=State.cargar_sala,
        background=COLORS["bg_primary"],
        min_height="100vh",
    )