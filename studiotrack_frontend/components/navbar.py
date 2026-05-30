# Barra de navegacion compartida por todas las paginas.
import reflex as rx

from studiotrack_frontend.theme import COLORS, FONT_DISPLAY, FONT_BODY


def navbar() -> rx.Component:
    return rx.hstack(
        rx.heading(
            "StudioTrack",
            font_family=FONT_DISPLAY,
            color=COLORS["accent_purple"],
            size="6",
        ),
        rx.spacer(),
        rx.link("Inicio", href="/", color=COLORS["text_primary"], font_family=FONT_BODY),
        rx.link("Reservar", href="/reservar", color=COLORS["text_primary"], font_family=FONT_BODY),
        width="100%",
        padding="1.2em 2em",
        background=COLORS["bg_surface"],
        border_bottom=f"1px solid {COLORS['border']}",
        align="center",
        position="sticky",
        top="0",
        z_index="10",
    )