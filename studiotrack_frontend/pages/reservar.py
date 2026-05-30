# Pagina de reserva: formulario de cliente, detalle, metodo de pago y confirmacion.
import reflex as rx

from studiotrack_frontend.theme import COLORS, FONT_DISPLAY, FONT_BODY
from studiotrack_frontend.state import State
from studiotrack_frontend.components.navbar import navbar


def _campo(label: str, placeholder: str, value, on_change, tipo: str = "text") -> rx.Component:
    return rx.vstack(
        rx.text(label, font_family=FONT_BODY, color=COLORS["text_primary"], font_size="0.9em"),
        rx.input(
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            type=tipo,
            background=COLORS["bg_card"],
            border=f"1px solid {COLORS['border']}",
            color=COLORS["text_primary"],
            border_radius="8px",
            width="100%",
        ),
        align="start",
        width="100%",
        spacing="1",
    )


def reservar() -> rx.Component:
    return rx.box(
        navbar(),
        rx.cond(
            State.reserva_ok,
            rx.vstack(
                rx.heading("Reserva confirmada", font_family=FONT_DISPLAY, color=COLORS["accent_teal"], size="7"),
                rx.text(
                    f"Total: ${State.reserva_total}",
                    font_family=FONT_BODY,
                    color=COLORS["accent_amber"],
                    font_size="1.3em",
                ),
                rx.text(
                    "Te contactaremos para confirmar el pago.",
                    font_family=FONT_BODY,
                    color=COLORS["text_muted"],
                ),
                rx.link(
                    rx.button(
                        "Volver al inicio",
                        background=COLORS["accent_purple"],
                        color="white",
                        border_radius="10px",
                        padding="0.8em 1.5em",
                        cursor="pointer",
                    ),
                    href="/",
                ),
                spacing="4",
                padding="4em 2em",
                align="center",
            ),
            rx.vstack(
                rx.heading("Reservar sala", font_family=FONT_DISPLAY, color=COLORS["text_primary"], size="7"),
                _campo("ID de sala", "Ej: 1", State.form_estudio_id, State.set_form_estudio_id),
                _campo("Nombre o banda", "Tu nombre", State.form_nombre, State.set_form_nombre),
                _campo("Email", "correo@ejemplo.com", State.form_email, State.set_form_email, "email"),
                _campo("Telefono", "809-000-0000", State.form_telefono, State.set_form_telefono),
                _campo("Fecha", "", State.form_fecha, State.set_form_fecha, "date"),
                _campo("Hora de inicio", "", State.form_hora, State.set_form_hora, "time"),
                _campo("Duracion (horas)", "1", State.form_duracion, State.set_form_duracion, "number"),
                rx.vstack(
                    rx.text("Metodo de pago", font_family=FONT_BODY, color=COLORS["text_primary"], font_size="0.9em"),
                    rx.select(
                        ["tarjeta", "transferencia", "efectivo"],
                        value=State.form_metodo,
                        on_change=State.set_form_metodo,
                        background=COLORS["bg_card"],
                        color=COLORS["text_primary"],
                        width="100%",
                    ),
                    align="start",
                    width="100%",
                    spacing="1",
                ),
                rx.cond(
                    State.reserva_error != "",
                    rx.text(State.reserva_error, color=COLORS["accent_coral"], font_family=FONT_BODY),
                ),
                rx.button(
                    "Confirmar reserva",
                    on_click=State.enviar_reserva,
                    background=COLORS["accent_purple"],
                    color="white",
                    border_radius="10px",
                    padding="0.9em 2em",
                    font_family=FONT_BODY,
                    font_weight="600",
                    cursor="pointer",
                    width="100%",
                ),
                spacing="3",
                max_width="500px",
                margin="0 auto",
                padding="2em",
                background=COLORS["bg_card"],
                border=f"1px solid {COLORS['border']}",
                border_radius="16px",
            ),
        ),
        background=COLORS["bg_primary"],
        min_height="100vh",
        padding_bottom="3em",
    )