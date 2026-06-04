# Panel de administracion: login + CRUD de salas y productos + listados.
import reflex as rx

from studiotrack_frontend.theme import COLORS, FONT_DISPLAY, FONT_BODY, CARD_STYLE
from studiotrack_frontend.state_admin import AdminState


# ---------- Helpers de estilo ----------
def _input(label, value, on_change, tipo="text"):
    return rx.vstack(
        rx.text(label, font_family=FONT_BODY, color=COLORS["text_muted"], font_size="0.8em"),
        rx.input(value=value, on_change=on_change, type=tipo,
                 background=COLORS["bg_card"], border=f"1px solid {COLORS['border']}",
                 color=COLORS["text_primary"], width="100%"),
        align="start", width="100%", spacing="1",
    )


def _boton(texto, on_click, color=None):
    return rx.button(texto, on_click=on_click,
                     background=color or COLORS["accent_purple"], color="white",
                     border_radius="8px", cursor="pointer", font_family=FONT_BODY,
                     style={"background_color": f"{color or COLORS['accent_purple']} !important"})


# ---------- Pantalla de login ----------
def _login() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Panel de administracion", font_family=FONT_DISPLAY,
                       color=COLORS["text_primary"], size="7"),
            rx.text("Acceso restringido", font_family=FONT_BODY, color=COLORS["text_muted"]),
            rx.input(placeholder="Clave de administrador", type="password",
                     value=AdminState.clave_input, on_change=AdminState.set_clave_input,
                     background=COLORS["bg_card"], border=f"1px solid {COLORS['border']}",
                     color=COLORS["text_primary"], width="100%"),
            rx.cond(AdminState.login_error != "",
                    rx.text(AdminState.login_error, color=COLORS["accent_coral"], font_family=FONT_BODY)),
            _boton("Entrar", AdminState.login),
            rx.link("← Volver al inicio", href="/", color=COLORS["text_muted"], font_family=FONT_BODY),
            spacing="4", width="360px", **CARD_STYLE,
        ),
        min_height="100vh", background=COLORS["bg_primary"],
    )


# ---------- Tabs ----------
def _tab_btn(label, value):
    return rx.button(
        label, on_click=lambda: AdminState.set_tab(value),
        background=rx.cond(AdminState.tab == value, COLORS["accent_purple"], "transparent"),
        color="white", border=f"1px solid {COLORS['accent_purple']}",
        border_radius="8px", cursor="pointer", font_family=FONT_BODY,
    )


# ---------- Panel de salas ----------
def _fila_sala(s: dict) -> rx.Component:
    return rx.hstack(
        rx.text(s["nombre"], color=COLORS["text_primary"], font_family=FONT_BODY, width="40%"),
        rx.text(s["tipo"], color=COLORS["text_muted"], font_family=FONT_BODY, width="20%"),
        rx.text(f"${s['precio_hora']}", color=COLORS["accent_amber"], font_family=FONT_BODY, width="15%"),
        rx.button("Editar", on_click=lambda: AdminState.editar_sala_form(s),
                  background=COLORS["accent_teal"], color="white", border_radius="6px",
                  cursor="pointer", size="1"),
        rx.button("Borrar", on_click=lambda: AdminState.eliminar_sala(s["id"]),
                  background=COLORS["accent_coral"], color="white", border_radius="6px",
                  cursor="pointer", size="1"),
        width="100%", padding="0.5em", border_bottom=f"1px solid {COLORS['border']}", align="center",
    )


def _panel_salas() -> rx.Component:
    return rx.vstack(
        rx.heading(rx.cond(AdminState.sala_id_edit == 0, "Nueva sala", "Editar sala"),
                   font_family=FONT_DISPLAY, color=COLORS["text_primary"], size="5"),
        _input("Nombre", AdminState.f_sala_nombre, AdminState.set_f_sala_nombre),
        _input("Descripcion", AdminState.f_sala_desc, AdminState.set_f_sala_desc),
        rx.hstack(
            rx.vstack(rx.text("Tipo", font_family=FONT_BODY, color=COLORS["text_muted"], font_size="0.8em"),
                      rx.select(["grabacion", "ensayo"], value=AdminState.f_sala_tipo,
                                on_change=AdminState.set_f_sala_tipo, width="100%"),
                      align="start", width="100%"),
            _input("Capacidad", AdminState.f_sala_capacidad, AdminState.set_f_sala_capacidad, "number"),
            _input("Precio/hora", AdminState.f_sala_precio, AdminState.set_f_sala_precio, "number"),
            width="100%", spacing="3",
        ),
        _input("URL imagen", AdminState.f_sala_imagen, AdminState.set_f_sala_imagen),
        rx.hstack(
            _boton("Guardar", AdminState.guardar_sala),
            _boton("Limpiar / Nuevo", AdminState.nueva_sala, COLORS["bg_card"]),
            spacing="3",
        ),
        rx.divider(margin_y="1em"),
        rx.heading("Salas existentes", font_family=FONT_DISPLAY, color=COLORS["text_primary"], size="4"),
        rx.foreach(AdminState.salas, _fila_sala),
        spacing="3", width="100%", **CARD_STYLE,
    )


# ---------- Panel de productos ----------
def _fila_prod(p: dict) -> rx.Component:
    return rx.hstack(
        rx.text(p["nombre"], color=COLORS["text_primary"], font_family=FONT_BODY, width="35%"),
        rx.text(p["tipo"], color=COLORS["text_muted"], font_family=FONT_BODY, width="15%"),
        rx.text(f"Stock: {p['stock']}", color=COLORS["text_muted"], font_family=FONT_BODY, width="15%"),
        rx.button("Editar", on_click=lambda: AdminState.editar_producto_form(p),
                  background=COLORS["accent_teal"], color="white", border_radius="6px",
                  cursor="pointer", size="1"),
        rx.button("Borrar", on_click=lambda: AdminState.eliminar_producto(p["id"]),
                  background=COLORS["accent_coral"], color="white", border_radius="6px",
                  cursor="pointer", size="1"),
        width="100%", padding="0.5em", border_bottom=f"1px solid {COLORS['border']}", align="center",
    )


def _panel_productos() -> rx.Component:
    return rx.vstack(
        rx.heading(rx.cond(AdminState.prod_id_edit == 0, "Nuevo producto", "Editar producto"),
                   font_family=FONT_DISPLAY, color=COLORS["text_primary"], size="5"),
        _input("Nombre", AdminState.f_prod_nombre, AdminState.set_f_prod_nombre),
        _input("Descripcion", AdminState.f_prod_desc, AdminState.set_f_prod_desc),
        rx.hstack(
            rx.vstack(rx.text("Tipo", font_family=FONT_BODY, color=COLORS["text_muted"], font_size="0.8em"),
                      rx.select(["venta", "alquiler", "ambos"], value=AdminState.f_prod_tipo,
                                on_change=AdminState.set_f_prod_tipo, width="100%"),
                      align="start", width="100%"),
            _input("Stock", AdminState.f_prod_stock, AdminState.set_f_prod_stock, "number"),
            width="100%", spacing="3",
        ),
        rx.hstack(
            _input("Precio venta", AdminState.f_prod_pventa, AdminState.set_f_prod_pventa, "number"),
            _input("Precio alquiler/dia", AdminState.f_prod_palq, AdminState.set_f_prod_palq, "number"),
            width="100%", spacing="3",
        ),
        _input("URL imagen", AdminState.f_prod_imagen, AdminState.set_f_prod_imagen),
        rx.hstack(
            _boton("Guardar", AdminState.guardar_producto),
            _boton("Limpiar / Nuevo", AdminState.nuevo_producto, COLORS["bg_card"]),
            spacing="3",
        ),
        rx.divider(margin_y="1em"),
        rx.heading("Productos existentes", font_family=FONT_DISPLAY, color=COLORS["text_primary"], size="4"),
        rx.foreach(AdminState.productos, _fila_prod),
        spacing="3", width="100%", **CARD_STYLE,
    )


# ---------- Panel de reservas ----------
def _fila_reserva(r: dict) -> rx.Component:
    return rx.hstack(
        rx.text(r["cliente_nombre"], color=COLORS["text_primary"], font_family=FONT_BODY, width="25%"),
        rx.text(r["cliente_email"], color=COLORS["text_muted"], font_family=FONT_BODY, width="30%"),
        rx.text(r["fecha"], color=COLORS["text_muted"], font_family=FONT_BODY, width="20%"),
        rx.text(f"${r['total']}", color=COLORS["accent_amber"], font_family=FONT_BODY, width="15%"),
        rx.text(r["estado"], color=COLORS["accent_teal"], font_family=FONT_BODY, width="10%"),
        width="100%", padding="0.5em", border_bottom=f"1px solid {COLORS['border']}",
    )


def _panel_reservas() -> rx.Component:
    return rx.vstack(
        rx.heading("Reservas registradas", font_family=FONT_DISPLAY, color=COLORS["text_primary"], size="5"),
        rx.foreach(AdminState.reservas, _fila_reserva),
        spacing="2", width="100%", **CARD_STYLE,
    )


# ---------- Panel de transacciones ----------
def _fila_trans(t: dict) -> rx.Component:
    return rx.hstack(
        rx.text(f"#{t['id']}", color=COLORS["text_muted"], font_family=FONT_BODY, width="10%"),
        rx.text(t["cliente_nombre"], color=COLORS["text_primary"], font_family=FONT_BODY, width="30%"),
        rx.text(t["cliente_email"], color=COLORS["text_muted"], font_family=FONT_BODY, width="35%"),
        rx.text(f"${t['total']}", color=COLORS["accent_amber"], font_family=FONT_BODY, width="15%"),
        width="100%", padding="0.5em", border_bottom=f"1px solid {COLORS['border']}",
    )


def _panel_trans() -> rx.Component:
    return rx.vstack(
        rx.heading("Compras y alquileres", font_family=FONT_DISPLAY, color=COLORS["text_primary"], size="5"),
        rx.foreach(AdminState.transacciones, _fila_trans),
        spacing="2", width="100%", **CARD_STYLE,
    )


# ---------- Pagina ----------
def admin() -> rx.Component:
    return rx.cond(
        AdminState.autenticado,
        rx.box(
            rx.hstack(
                rx.heading("Admin StudioTrack", font_family=FONT_DISPLAY,
                           color=COLORS["accent_purple"], size="6"),
                rx.spacer(),
                rx.link("Ver sitio", href="/", color=COLORS["text_muted"], font_family=FONT_BODY),
                _boton("Cerrar sesion", AdminState.logout, COLORS["accent_coral"]),
                width="100%", padding="1.2em 2em", background=COLORS["bg_surface"],
                border_bottom=f"1px solid {COLORS['border']}", align="center",
            ),
            rx.hstack(
                _tab_btn("Salas", "salas"),
                _tab_btn("Productos", "productos"),
                _tab_btn("Reservas", "reservas"),
                _tab_btn("Transacciones", "transacciones"),
                spacing="3", padding="1.5em 2em",
            ),
            rx.cond(AdminState.mensaje != "",
                    rx.text(AdminState.mensaje, color=COLORS["accent_teal"],
                            font_family=FONT_BODY, padding_x="2em")),
            rx.box(
                rx.match(
                    AdminState.tab,
                    ("salas", _panel_salas()),
                    ("productos", _panel_productos()),
                    ("reservas", _panel_reservas()),
                    ("transacciones", _panel_trans()),
                    _panel_salas(),
                ),
                padding="0 2em 3em 2em",
            ),
            background=COLORS["bg_primary"], min_height="100vh",
        ),
        _login(),
    )