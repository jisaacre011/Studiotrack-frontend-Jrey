# Estado global de la aplicacion Reflex.
# Maneja: catalogo de estudios, detalle de sala y el formulario de reserva.
import reflex as rx
from typing import Any
from studiotrack_frontend import api


class State(rx.State):
    # --- Catalogo (pagina index) ---
    estudios: list[dict] = []
    cargando: bool = False
    error: str = ""
    planes: list[dict] = []

    # --- Detalle de sala (pagina sala) ---
    sala_actual: dict[str, Any] = {}
    equipos: list[dict[str, Any]] = []

    # --- Formulario de reserva (pagina reservar) ---
    form_estudio_id: str = ""
    form_nombre: str = ""
    form_email: str = ""
    form_telefono: str = ""
    form_fecha: str = ""
    form_hora: str = ""
    form_duracion: str = "1"
    form_metodo: str = "tarjeta"

    # Resultado de la reserva.
    reserva_ok: bool = False
    reserva_total: float = 0.0
    reserva_error: str = ""

    # Setters manuales para los campos del formulario.
    def set_form_estudio_id(self, val: str): self.form_estudio_id = val
    def set_form_nombre(self, val: str): self.form_nombre = val
    def set_form_email(self, val: str): self.form_email = val
    def set_form_telefono(self, val: str): self.form_telefono = val
    def set_form_fecha(self, val: str): self.form_fecha = val
    def set_form_hora(self, val: str): self.form_hora = val
    def set_form_duracion(self, val: str): self.form_duracion = val
    def set_form_metodo(self, val: str): self.form_metodo = val

    async def cargar_estudios(self):
        """Carga el catalogo desde la API. Se dispara al montar la pagina."""
        self.cargando = True
        self.error = ""
        try:
            self.estudios = await api.get_estudios()
        except Exception:
            self.error = "No se pudo cargar el catalogo. Verifica que el backend este corriendo."
        finally:
            self.cargando = False

    async def cargar_sala(self):
        """Carga el detalle de una sala usando el id de la URL."""
        self.error = ""
        try:
            sala_id = int(self.router.page.params.get("id", 0))
            data = await api.get_estudio(sala_id)
            self.sala_actual = data
            self.equipos = data.get("equipos", [])
        except Exception:
            self.error = "No se pudo cargar la sala."
            self.sala_actual = {}
            self.equipos = []

    def ir_a_reservar(self, estudio_id: int):
        """Navega a la pagina de reserva preseleccionando la sala."""
        self.form_estudio_id = str(estudio_id)
        return rx.redirect("/reservar")

    async def enviar_reserva(self):
        """Valida y envia la reserva al backend."""
        self.reserva_error = ""
        self.reserva_ok = False

        if not (self.form_estudio_id and self.form_nombre and self.form_email
                and self.form_fecha and self.form_hora):
            self.reserva_error = "Completa todos los campos obligatorios."
            return

        payload = {
            "estudio_id": int(self.form_estudio_id),
            "cliente_nombre": self.form_nombre,
            "cliente_email": self.form_email,
            "cliente_telefono": self.form_telefono or None,
            "fecha": self.form_fecha,
            "hora_inicio": self.form_hora if len(self.form_hora) == 8 else f"{self.form_hora}:00",
            "duracion_horas": int(self.form_duracion),
            "metodo_pago": self.form_metodo,
        }

        try:
            resultado = await api.crear_reserva(payload)
            self.reserva_ok = True
            self.reserva_total = float(resultado["total"])
        except Exception:
            self.reserva_error = "No se pudo registrar la reserva. Revisa los datos e intenta de nuevo."

    async def cargar_planes(self):
        try:
            self.planes = await api.get_planes()
        except Exception:
            pass

