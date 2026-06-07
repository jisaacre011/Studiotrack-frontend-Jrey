# Estado de la tienda: catalogo de productos y carrito del cliente.
import reflex as rx

from studiotrack_frontend import api


class TiendaState(rx.State):
    productos: list[dict] = []
    cargando: bool = False
    error: str = ""

    # Carrito: lista de items que el cliente va agregando.
    # Cada item: {producto_id, nombre, modalidad, cantidad, dias, precio_unit, subtotal}
    carrito: list[dict] = []

    # Datos del cliente para la factura.
    cli_nombre: str = ""
    cli_email: str = ""
    cli_telefono: str = ""

    # Resultado.
    factura_ok: bool = False
    factura_total: float = 0.0
    factura_error: str = ""

    def set_cli_nombre(self, val: str): self.cli_nombre = val
    def set_cli_email(self, val: str): self.cli_email = val
    def set_cli_telefono(self, val: str): self.cli_telefono = val

    async def cargar_productos(self):
        self.cargando = True
        self.error = ""
        try:
            self.productos = await api.get_productos()
        except Exception:
            self.error = "No se pudo cargar la tienda. Verifica que el backend este activo."
        finally:
            self.cargando = False

    def agregar_al_carrito(self, producto: dict, modalidad: str):
        # Calcula precio segun modalidad y agrega al carrito (cantidad 1, 1 dia por defecto).
        if modalidad == "compra":
            precio = float(producto["precio_venta"] or 0)
            subtotal = precio
            dias = 1
        else:  # alquiler
            precio = float(producto["precio_alquiler_dia"] or 0)
            subtotal = precio  # 1 dia x 1 unidad
            dias = 1

        self.carrito = self.carrito + [{
            "producto_id": producto["id"],
            "nombre": producto["nombre"],
            "modalidad": modalidad,
            "cantidad": 1,
            "dias": dias,
            "precio_unit": precio,
            "subtotal": subtotal,
        }]

    def quitar_del_carrito(self, index: int):
        self.carrito = [it for i, it in enumerate(self.carrito) if i != index]

    def cambiar_cantidad(self, index: int, delta: int):
        nuevo = []
        for i, it in enumerate(self.carrito):
            if i == index:
                it = dict(it)
                it["cantidad"] = max(1, it["cantidad"] + delta)
                it["subtotal"] = it["precio_unit"] * it["cantidad"] * it["dias"]
            nuevo.append(it)
        self.carrito = nuevo

    def cambiar_dias(self, index: int, delta: int):
        nuevo = []
        for i, it in enumerate(self.carrito):
            if i == index:
                it = dict(it)
                if it["modalidad"] == "alquiler":
                    it["dias"] = max(1, it["dias"] + delta)
                    it["subtotal"] = it["precio_unit"] * it["cantidad"] * it["dias"]
            nuevo.append(it)
        self.carrito = nuevo

    @rx.var
    def total_carrito(self) -> float:
        return sum(it["subtotal"] for it in self.carrito)

    @rx.var
    def carrito_vacio(self) -> bool:
        return len(self.carrito) == 0

    async def confirmar_compra(self):
        self.factura_error = ""
        self.factura_ok = False
        if not self.carrito:
            self.factura_error = "El carrito esta vacio."
            return
        if not (self.cli_nombre and self.cli_email):
            self.factura_error = "Completa nombre y email."
            return

        payload = {
            "cliente_nombre": self.cli_nombre,
            "cliente_email": self.cli_email,
            "cliente_telefono": self.cli_telefono or None,
            "items": [
                {"producto_id": it["producto_id"], "modalidad": it["modalidad"],
                 "cantidad": it["cantidad"], "dias": it["dias"]}
                for it in self.carrito
            ],
        }
        try:
            resultado = await api.crear_transaccion(payload)
            self.factura_ok = True
            self.factura_total = float(resultado["total"])
            self.carrito = []
        except Exception:
            self.factura_error = "No se pudo procesar la compra. Intenta de nuevo."
