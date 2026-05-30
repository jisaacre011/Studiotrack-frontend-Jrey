# Card de una sala para el catalogo de la pagina de inicio.
import reflex as rx

from studiotrack_frontend.theme import COLORS, FONT_DISPLAY, FONT_BODY, CARD_STYLE
from studiotrack_frontend.state import State


def sala_card(estudio: dict) -> rx.Component:
    return rx.box(
        rx.image(
            src=estudio["imagen_url"],
            width="100%",
            height="180px",
            object_fit="cover",
            border_radius="12px",
        ),
        rx.heading(
            estudio["nombre"],
            font_family=FONT_DISPLAY,
            color=COLORS["text_primary"],
            size="5",
            margin_top="0.6em",
        ),
        rx.text(
            estudio["tipo"],
            font_family=FONT_BODY,
            color=COLORS["text_muted"],
            font_size="0.85em",
        ),
        rx.hstack(
            rx.text(
                f"${estudio['precio_hora']}/hora",
                font_family=FONT_BODY,
                color=COLORS["accent_amber"],
                font_weight="600",
            ),
            rx.spacer(),
            rx.text(
                f"Cap. {estudio['capacidad']}",
                font_family=FONT_BODY,
                color=COLORS["text_muted"],
            ),
            width="100%",
            margin_top="0.5em",
        ),
        rx.hstack(
            rx.link(
                rx.button(
                    "Ver detalle",
                    background="transparent",
                    color=COLORS["accent_purple"],
                    border=f"1px solid {COLORS['accent_purple']}",
                    border_radius="8px",
                    cursor="pointer",
                ),
                href=f"/sala/{estudio['id']}",
            ),
            rx.button(
                "Reservar",
                on_click=lambda: State.ir_a_reservar(estudio["id"]),
                background=COLORS["accent_purple"],
                color="white",
                border_radius="8px",
                cursor="pointer",
            ),
            spacing="3",
            margin_top="1em",
        ),
        **CARD_STYLE,
        width="320px",
    )