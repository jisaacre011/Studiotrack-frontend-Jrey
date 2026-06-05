import reflex as rx
from studiotrack_frontend.theme import COLORS, FONT_BODY

_SCROLL_ID = "carrusel-scroll"


def carrusel(items: rx.Component, scroll_id: str = _SCROLL_ID, con_flechas: bool = True) -> rx.Component:
    contenedor = rx.box(
        items,
        id=scroll_id,
        display="flex",
        flex_direction="row",
        gap="1.5em",
        overflow_x="auto",
        padding="1em 2em 1.5em 2em",
        scroll_behavior="smooth",
        style={
            "scrollbarWidth": "thin",
            "scrollbarColor": f"{COLORS['accent_purple']} transparent",
            "&::-webkit-scrollbar": {"height": "8px"},
            "&::-webkit-scrollbar-thumb": {
                "background": COLORS["accent_purple"],
                "borderRadius": "4px",
            },
            "& > *": {"flexShrink": "0"},
        },
        max_width="1450px",
        margin="0 auto",
        width="100%",
    )
    if not con_flechas:
        return contenedor

    def _flecha(simbolo: str, desplazamiento: int) -> rx.Component:
        return rx.button(
            simbolo,
            on_click=rx.call_script(
                f"document.getElementById('{scroll_id}')"
                f".scrollBy({{left: {desplazamiento}, behavior: 'smooth'}})"
            ),
            background=COLORS["bg_card"],
            color=COLORS["text_primary"],
            border=f"1px solid {COLORS['accent_purple']}",
            border_radius="50%",
            width="40px",
            height="40px",
            cursor="pointer",
            font_family=FONT_BODY,
            font_size="1.2em",
            style={"pointerEvents": "auto"},
        )

    return rx.box(
        rx.hstack(
            _flecha("<", -700),
            rx.spacer(),
            _flecha(">", 700),
            width="100%",
            padding_x="2em",
            position="absolute",
            top="40%",
            z_index="5",
            style={"pointerEvents": "none"},
        ),
        contenedor,
        position="relative",
        width="100%",
    )