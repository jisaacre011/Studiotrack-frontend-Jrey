# Estado del panel de administracion: login, datos y formularios CRUD.
import reflex as rx

from studiotrack_frontend import api


class AdminState(rx.State):
    autenticado: bool = False
    clave_input: str = ""
    login_error: str = ""

    salas: list[dict] = []
    productos: list[dict] = []
    reservas: list[dict] = []
    transacciones: list[dict] = []

    tab: str = "salas"

    sala_id_edit: int = 0
    f_sala_nombre: str = ""
    f_sala_desc: str = ""
    f_sala_tipo: str = "grabacion"
    f_sala_capacidad: str = "2"
    f_sala_precio: str = ""
    f_sala_imagen: str = ""

    prod_id_edit: int = 0
    f_prod_nombre: str = ""
    f_prod_desc: str = ""
    f_prod_tipo: str = "venta"
    f_prod_pventa: str = ""
    f_prod_palq: str = ""
    f_prod_stock: str = "0"
    f_prod_imagen: str = ""

    mensaje: str = ""

    def set_clave_input(self, val: str): self.clave_input = val
    def set_f_sala_nombre(self, val: str): self.f_sala_nombre = val
    def set_f_sala_desc(self, val: str): self.f_sala_desc = val
    def set_f_sala_tipo(self, val: str): self.f_sala_tipo = val
    def set_f_sala_capacidad(self, val: str): self.f_sala_capacidad = val
    def set_f_sala_precio(self, val: str): self.f_sala_precio = val
    def set_f_sala_imagen(self, val: str): self.f_sala_imagen = val
    def set_f_prod_nombre(self, val: str): self.f_prod_nombre = val
    def set_f_prod_desc(self, val: str): self.f_prod_desc = val
    def set_f_prod_tipo(self, val: str): self.f_prod_tipo = val
    def set_f_prod_pventa(self, val: str): self.f_prod_pventa = val
    def set_f_prod_palq(self, val: str): self.f_prod_palq = val
    def set_f_prod_stock(self, val: str): self.f_prod_stock = val
    def set_f_prod_imagen(self, val: str): self.f_prod_imagen = val

    @rx.var
    def clave(self) -> str:
        return self.clave_input

    async def login(self):
        self.login_error = ""
        try:
            ok = await api.admin_login(self.clave_input)
            if ok:
                self.autenticado = True
                await self.cargar_todo()
            else:
                self.login_error = "Clave incorrecta."
        except Exception:
            self.login_error = "No se pudo conectar con el servidor."

    def logout(self):
        self.autenticado = False
        self.clave_input = ""

    def set_tab(self, t: str):
        self.tab = t

    async def cargar_todo(self):
        try:
            self.salas = await api.get_estudios()
            self.productos = await api.get_productos()
            self.reservas = await api.get_reservas(self.clave_input)
            self.transacciones = await api.get_transacciones(self.clave_input)
        except Exception:
            self.mensaje = "Error al cargar datos."

    def nueva_sala(self):
        self.sala_id_edit = 0
        self.f_sala_nombre = ""
        self.f_sala_desc = ""
        self.f_sala_tipo = "grabacion"
        self.f_sala_capacidad = "2"
        self.f_sala_precio = ""
        self.f_sala_imagen = ""

    def editar_sala_form(self, sala: dict):
        self.sala_id_edit = sala["id"]
        self.f_sala_nombre = sala["nombre"]
        self.f_sala_desc = sala["descripcion"] or ""
        self.f_sala_tipo = sala["tipo"]
        self.f_sala_capacidad = str(sala["capacidad"])
        self.f_sala_precio = str(sala["precio_hora"])
        self.f_sala_imagen = sala["imagen_url"] or ""

    async def guardar_sala(self):
        self.mensaje = ""
        data = {
            "nombre": self.f_sala_nombre,
            "descripcion": self.f_sala_desc or None,
            "tipo": self.f_sala_tipo,
            "capacidad": int(self.f_sala_capacidad or 1),
            "precio_hora": float(self.f_sala_precio or 0),
            "imagen_url": self.f_sala_imagen or None,
            "activo": True,
        }
        try:
            if self.sala_id_edit == 0:
                await api.crear_estudio(data, self.clave_input)
                self.mensaje = "Sala creada."
            else:
                await api.editar_estudio(self.sala_id_edit, data, self.clave_input)
                self.mensaje = "Sala actualizada."
            self.salas = await api.get_estudios()
            self.nueva_sala()
        except Exception:
            self.mensaje = "Error al guardar la sala. Revisa los datos."

    async def eliminar_sala(self, sid: int):
        self.mensaje = ""
        try:
            await api.borrar_estudio(sid, self.clave_input)
            self.salas = await api.get_estudios()
            self.mensaje = "Sala eliminada."
        except Exception:
            self.mensaje = "No se pudo eliminar (puede tener reservas asociadas)."

    def nuevo_producto(self):
        self.prod_id_edit = 0
        self.f_prod_nombre = ""
        self.f_prod_desc = ""
        self.f_prod_tipo = "venta"
        self.f_prod_pventa = ""
        self.f_prod_palq = ""
        self.f_prod_stock = "0"
        self.f_prod_imagen = ""

    def editar_producto_form(self, p: dict):
        self.prod_id_edit = p["id"]
        self.f_prod_nombre = p["nombre"]
        self.f_prod_desc = p["descripcion"] or ""
        self.f_prod_tipo = p["tipo"]
        self.f_prod_pventa = str(p["precio_venta"]) if p["precio_venta"] else ""
        self.f_prod_palq = str(p["precio_alquiler_dia"]) if p["precio_alquiler_dia"] else ""
        self.f_prod_stock = str(p["stock"])
        self.f_prod_imagen = p["imagen_url"] or ""

    async def guardar_producto(self):
        self.mensaje = ""
        data = {
            "nombre": self.f_prod_nombre,
            "descripcion": self.f_prod_desc or None,
            "tipo": self.f_prod_tipo,
            "precio_venta": float(self.f_prod_pventa) if self.f_prod_pventa else None,
            "precio_alquiler_dia": float(self.f_prod_palq) if self.f_prod_palq else None,
            "stock": int(self.f_prod_stock or 0),
            "imagen_url": self.f_prod_imagen or None,
            "activo": True,
        }
        try:
            if self.prod_id_edit == 0:
                await api.crear_producto(data, self.clave_input)
                self.mensaje = "Producto creado."
            else:
                await api.editar_producto(self.prod_id_edit, data, self.clave_input)
                self.mensaje = "Producto actualizado."
            self.productos = await api.get_productos()
            self.nuevo_producto()
        except Exception:
            self.mensaje = "Error al guardar el producto."

    async def eliminar_producto(self, pid: int):
        self.mensaje = ""
        try:
            await api.borrar_producto(pid, self.clave_input)
            self.productos = await api.get_productos()
            self.mensaje = "Producto eliminado."
        except Exception:
            self.mensaje = "No se pudo eliminar el producto."
