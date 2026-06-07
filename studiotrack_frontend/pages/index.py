# Pagina de inicio: hero, catalogo de salas, planes y contacto.
import reflex as rx
from studiotrack_frontend.theme import COLORS, FONT_DISPLAY, FONT_BODY, CARD_STYLE
from studiotrack_frontend.state import State
from studiotrack_frontend.components.navbar import navbar
from studiotrack_frontend.components.sala_card import sala_card
from studiotrack_frontend.components.carrusel import carrusel


def _plan_card(plan: dict) -> rx.Component:
    return rx.box(
        rx.heading(plan["nombre"], font_family=FONT_DISPLAY, color=COLORS["accent_purple"], size="5"),
        rx.text(plan["descripcion"], font_family=FONT_BODY, color=COLORS["text_muted"],
                font_size="0.85em", margin_y="0.8em"),
        rx.text(f"${plan['precio']}", font_family=FONT_DISPLAY, color=COLORS["accent_amber"],
                size="7", font_weight="700"),
        rx.link(
            rx.button("Reservar plan", background=COLORS["accent_coral"], color="white",
                      border_radius="8px", cursor="pointer", font_family=FONT_BODY,
                      style={"background_color": f"{COLORS['accent_coral']} !important"}),
            href="/reservar",
        ),
        width="300px", **CARD_STYLE,
    )


def index() -> rx.Component:
    return rx.box(
        navbar(),
        rx.vstack(
            rx.heading(
                "Tu sonido empieza aqui",
                font_family=FONT_DISPLAY,
                color=COLORS["text_primary"],
                size="9",
                text_align="center",
            ),
            rx.text(
                "Reserva estudios de grabacion y salas de ensayo profesionales.",
                font_family=FONT_BODY,
                color=COLORS["text_muted"],
                text_align="center",
                font_size="1.1em",
            ),
            rx.link(
                rx.button(
                    "Reservar ahora",
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
            spacing="5",
            padding="5em 2em",
            align="center",
        ),
        rx.heading(
            "Nuestras salas",
            font_family=FONT_DISPLAY,
            color=COLORS["text_primary"],
            size="7",
            padding_left="2em",
        ),
        rx.cond(
            State.cargando,
            rx.text("Cargando...", color=COLORS["text_muted"], padding="2em"),
            rx.cond(
                State.error != "",
                rx.text(State.error, color=COLORS["accent_coral"], padding="2em"),
                carrusel(
                    rx.foreach(State.estudios, sala_card),
                    scroll_id="carrusel-salas",
                    con_flechas=True,
                ),
            ),
        ),
        rx.heading("Planes y ofertas", font_family=FONT_DISPLAY, color=COLORS["text_primary"],
                   size="7", padding_left="2em", margin_top="2em"),
        rx.flex(
            rx.foreach(State.planes, _plan_card),
            wrap="wrap", gap="1.5em", justify="center", padding="2em",
        ),
        rx.heading("Equipos en venta y alquiler", font_family=FONT_DISPLAY,
                   color=COLORS["text_primary"], size="7", padding_left="2em", margin_top="2em"),
        rx.text("Visita nuestra tienda de equipos profesionales.",
                font_family=FONT_BODY, color=COLORS["text_muted"], padding_left="2em"),
        rx.center(
            rx.link(
                rx.button("Ir a la tienda", background=COLORS["accent_purple"], color="white",
                          border_radius="10px", padding="0.9em 2em", font_family=FONT_BODY,
                          font_weight="600", cursor="pointer"),
                href="/tienda",
            ),
            padding="1.5em",
        ),
        rx.box(
            rx.heading("Contacto", font_family=FONT_DISPLAY, color=COLORS["text_primary"], size="6"),
            rx.text(
                "StudioTrack — Santo Domingo. Tel: 849-215-2599. byshokcomusiic@gmail.com",
                font_family=FONT_BODY,
                color=COLORS["text_muted"],
            ),
            padding="2em",
            background=COLORS["bg_surface"],
            border_top=f"1px solid {COLORS['border']}",
            margin_top="3em",
        ),
        on_mount=[State.cargar_estudios, State.cargar_planes],
        background=COLORS["bg_primary"],
        min_height="100vh",
    )
