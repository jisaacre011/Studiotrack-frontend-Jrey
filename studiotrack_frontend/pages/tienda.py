# Tienda: catalogo de productos (venta/alquiler) y carrito con factura.
import reflex as rx

from studiotrack_frontend.theme import COLORS, FONT_DISPLAY, FONT_BODY, CARD_STYLE
from studiotrack_frontend.state_tienda import TiendaState
from studiotrack_frontend.components.navbar import navbar


def _producto_card(p: dict) -> rx.Component:
    return rx.box(
        rx.image(src=p["imagen_url"], width="100%", height="160px",
                 object_fit="cover", border_radius="12px"),
        rx.heading(p["nombre"], font_family=FONT_DISPLAY, color=COLORS["text_primary"],
                   size="4", margin_top="0.5em"),
        rx.text(p["descripcion"], font_family=FONT_BODY, color=COLORS["text_muted"],
                font_size="0.8em", no_of_lines=2),
        # Precios segun lo que ofrezca.
        rx.cond(p["precio_venta"],
                rx.text(f"Venta: ${p['precio_venta']}", font_family=FONT_BODY,
                        color=COLORS["accent_amber"], font_weight="600")),
        rx.cond(p["precio_alquiler_dia"],
                rx.text(f"Alquiler: ${p['precio_alquiler_dia']}/dia", font_family=FONT_BODY,
                        color=COLORS["accent_teal"], font_weight="600")),
        # Botones segun modalidad disponible.
        rx.hstack(
            rx.cond(p["precio_venta"],
                    rx.button("Comprar", on_click=lambda: TiendaState.agregar_al_carrito(p, "compra"),
                              background=COLORS["accent_amber"], color="black",
                              border_radius="8px", cursor="pointer", size="1",
                              font_family=FONT_BODY, font_weight="600")),
            rx.cond(p["precio_alquiler_dia"],
                    rx.button("Alquilar", on_click=lambda: TiendaState.agregar_al_carrito(p, "alquiler"),
                              background=COLORS["accent_teal"], color="white",
                              border_radius="8px", cursor="pointer", size="1",
                              font_family=FONT_BODY, font_weight="600")),
            spacing="2", margin_top="0.5em",
        ),
        **CARD_STYLE, width="260px",
    )


def _item_carrito(item: rx.Var, index: int) -> rx.Component:
    return rx.hstack(
        rx.vstack(
            rx.text(item["nombre"], color=COLORS["text_primary"], font_family=FONT_BODY,
                    font_weight="600", font_size="0.9em"),
            rx.text(item["modalidad"], color=COLORS["text_muted"], font_family=FONT_BODY,
                    font_size="0.75em"),
            align="start", spacing="0", width="40%",
        ),
        # Cantidad.
        rx.hstack(
            rx.button("-", on_click=lambda: TiendaState.cambiar_cantidad(index, -1), size="1",
                      background=COLORS["bg_card"], cursor="pointer"),
            rx.text(item["cantidad"], color=COLORS["text_primary"], font_family=FONT_BODY),
            rx.button("+", on_click=lambda: TiendaState.cambiar_cantidad(index, 1), size="1",
                      background=COLORS["bg_card"], cursor="pointer"),
            spacing="1", align="center",
        ),
        # Dias (solo alquiler).
        rx.cond(
            item["modalidad"] == "alquiler",
            rx.hstack(
                rx.button("-", on_click=lambda: TiendaState.cambiar_dias(index, -1), size="1",
                          background=COLORS["bg_card"], cursor="pointer"),
                rx.text(f"{item['dias']}d", color=COLORS["text_primary"], font_family=FONT_BODY),
                rx.button("+", on_click=lambda: TiendaState.cambiar_dias(index, 1), size="1",
                          background=COLORS["bg_card"], cursor="pointer"),
                spacing="1", align="center",
            ),
            rx.text("—", color=COLORS["text_muted"], font_family=FONT_BODY),
        ),
        rx.text(f"${item['subtotal']}", color=COLORS["accent_amber"], font_family=FONT_BODY,
                width="15%"),
        rx.button("x", on_click=lambda: TiendaState.quitar_del_carrito(index), size="1",
                  background=COLORS["accent_coral"], color="white", cursor="pointer"),
        width="100%", padding="0.5em", border_bottom=f"1px solid {COLORS['border']}",
        align="center", justify="between",
    )


def _carrito() -> rx.Component:
    return rx.box(
        rx.heading("Tu carrito", font_family=FONT_DISPLAY, color=COLORS["text_primary"], size="6"),
        rx.cond(
            TiendaState.carrito_vacio,
            rx.text("Agrega productos para comprar o alquilar.", color=COLORS["text_muted"],
                    font_family=FONT_BODY),
            rx.vstack(
                rx.foreach(TiendaState.carrito, _item_carrito),
                rx.hstack(
                    rx.spacer(),
                    rx.text("Total:", color=COLORS["text_primary"], font_family=FONT_BODY,
                            font_weight="600"),
                    rx.text(f"${TiendaState.total_carrito}", color=COLORS["accent_amber"],
                            font_family=FONT_BODY, font_weight="700", font_size="1.2em"),
                    width="100%", padding="0.5em",
                ),
                # Datos del cliente.
                rx.input(placeholder="Nombre o banda", value=TiendaState.cli_nombre,
                         on_change=TiendaState.set_cli_nombre, background=COLORS["bg_card"],
                         color=COLORS["text_primary"], width="100%"),
                rx.input(placeholder="Email", type="email", value=TiendaState.cli_email,
                         on_change=TiendaState.set_cli_email, background=COLORS["bg_card"],
                         color=COLORS["text_primary"], width="100%"),
                rx.input(placeholder="Telefono", value=TiendaState.cli_telefono,
                         on_change=TiendaState.set_cli_telefono, background=COLORS["bg_card"],
                         color=COLORS["text_primary"], width="100%"),
                rx.cond(TiendaState.factura_error != "",
                        rx.text(TiendaState.factura_error, color=COLORS["accent_coral"],
                                font_family=FONT_BODY)),
                rx.button("Confirmar y generar factura", on_click=TiendaState.confirmar_compra,
                          background=COLORS["accent_purple"], color="white", border_radius="10px",
                          cursor="pointer", font_family=FONT_BODY, font_weight="600", width="100%",
                          style={"background_color": f"{COLORS['accent_purple']} !important"}),
                spacing="3", width="100%",
            ),
        ),
        **CARD_STYLE, width="100%",
    )


def tienda() -> rx.Component:
    return rx.box(
        navbar(),
        rx.cond(
            TiendaState.factura_ok,
            # Confirmacion / factura.
            rx.center(
                rx.vstack(
                    rx.heading("Factura generada", font_family=FONT_DISPLAY,
                               color=COLORS["accent_teal"], size="7"),
                    rx.text(f"Total pagado: ${TiendaState.factura_total}", font_family=FONT_BODY,
                            color=COLORS["accent_amber"], font_size="1.3em"),
                    rx.text("Gracias por tu orden. Te contactaremos para coordinar.",
                            font_family=FONT_BODY, color=COLORS["text_muted"]),
                    rx.link(rx.button("Seguir comprando", background=COLORS["accent_purple"],
                                      color="white", border_radius="10px", cursor="pointer"),
                            href="/tienda"),
                    spacing="4", **CARD_STYLE,
                ),
                min_height="70vh",
            ),
            rx.vstack(
                rx.heading("Tienda de equipos", font_family=FONT_DISPLAY,
                           color=COLORS["text_primary"], size="8", padding_top="1em"),
                rx.text("Compra o alquila equipo profesional de audio y musica.",
                        font_family=FONT_BODY, color=COLORS["text_muted"]),
                rx.cond(
                    TiendaState.error != "",
                    rx.text(TiendaState.error, color=COLORS["accent_coral"], font_family=FONT_BODY),
                    rx.flex(
                        rx.foreach(TiendaState.productos, _producto_card),
                        wrap="wrap", gap="1.5em", justify="center", padding="2em 0",
                    ),
                ),
                _carrito(),
                spacing="4", padding="0 2em 3em 2em", max_width="1100px", margin="0 auto",
            ),
        ),
        on_mount=TiendaState.cargar_productos,
        background=COLORS["bg_primary"], min_height="100vh",
    )
