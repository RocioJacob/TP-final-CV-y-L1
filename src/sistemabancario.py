from __future__ import annotations
from typing import List, Optional
from datetime import datetime
import uuid
import traceback

# ---------- MODELOS ----------
class Cliente:
    def __init__(self, nombre: str, apellido: str, dni: str):
        self.__nombre = None
        self.__apellido = None
        self.__dni = None
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni

    # Getters / setters con validación mínima
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, val: str):
        if not isinstance(val, str) or not val.strip():
            raise ValueError("Nombre inválido")
        self.__nombre = val.strip()

    @property
    def apellido(self) -> str:
        return self.__apellido

    @apellido.setter
    def apellido(self, val: str):
        if not isinstance(val, str) or not val.strip():
            raise ValueError("Apellido inválido")
        self.__apellido = val.strip()

    @property
    def dni(self) -> str:
        return self.__dni

    @dni.setter
    def dni(self, val: str):
        if not isinstance(val, str) or not val.strip() or not val.strip().isdigit():
            raise ValueError("DNI debe ser numérico y no vacío")
        self.__dni = val.strip()

    def mostrar_datos(self) -> dict:
        return {"nombre": self.nombre, "apellido": self.apellido, "dni": self.dni}

    def __repr__(self):
        return f"Cliente({self.nombre} {self.apellido}, DNI={self.dni})"


class Transaccion:
    def __init__(self, tipo: str, monto: float, fecha: Optional[datetime] = None):
        if tipo not in ("DEP", "RET"):
            raise ValueError("Tipo de transacción debe ser 'DEP' o 'RET'")
        if monto <= 0:
            raise ValueError("El monto debe ser mayor que 0")
        self.__tipo = tipo
        self.__monto = float(monto)
        self.__fecha = fecha or datetime.now()
        self.__id = str(uuid.uuid4())

    @property
    def tipo(self) -> str:
        return self.__tipo

    @property
    def monto(self) -> float:
        return self.__monto

    @property
    def fecha(self) -> datetime:
        return self.__fecha

    def to_dict(self) -> dict:
        return {"id": self.__id, "tipo": self.tipo, "monto": self.monto, "fecha": self.fecha.isoformat()}

    def __repr__(self):
        return f"Transaccion({self.tipo}, {self.monto}, {self.fecha.isoformat()})"


class Cuenta:
    def __init__(self, cliente: Cliente):
        # atributos privados
        self.__numero_cuenta = self._generar_numero()
        self.__saldo = 0.0
        self.__cliente = cliente
        self.__transacciones: List[Transaccion] = []

    # Encapsulamiento
    @property
    def numero_cuenta(self) -> str:
        return self.__numero_cuenta

    @property
    def saldo(self) -> float:
        return self.__saldo

    @property
    def cliente(self) -> Cliente:
        return self.__cliente

    def _generar_numero(self) -> str:
        return str(uuid.uuid4())[:8]

    # Métodos - polimorfismo posible reimplementando en subclases
    def ingresar(self, monto: float) -> Transaccion:
        if monto <= 0:
            raise ValueError("El monto a ingresar debe ser mayor que cero")
        self.__saldo += monto
        tx = Transaccion("DEP", monto)
        self.__transacciones.append(tx)
        return tx

    def retirar(self, monto: float) -> Transaccion:
        if monto <= 0:
            raise ValueError("El monto a retirar debe ser mayor que cero")
        if monto > self.__saldo:
            raise ValueError("Saldo insuficiente")
        self.__saldo -= monto
        tx = Transaccion("RET", monto)
        self.__transacciones.append(tx)
        return tx

    def registrar_transaccion(self, tx: Transaccion):
        # permite registrar transacciones externas (p.ej. transferencia interna)
        self.__transacciones.append(tx)

    def obtener_transacciones(self) -> List[Transaccion]:
        return list(self.__transacciones)

    def mostrar_datos(self) -> dict:
        return {"numero_cuenta": self.numero_cuenta, "saldo": self.saldo, "cliente": self.cliente.mostrar_datos()}

    def __repr__(self):
        return f"Cuenta({self.numero_cuenta}, Saldo={self.saldo})"


# Subclases para herencia y polimorfismo
class CuentaAhorro(Cuenta):
    def __init__(self, cliente: Cliente, tasa_interes: float = 0.01):
        super().__init__(cliente)
        self.__tasa_interes = tasa_interes

    def aplicar_interes(self):
        # ejemplo simple: aplicar interes sobre saldo
        interes = self.saldo * self.__tasa_interes
        if interes > 0:
            self.ingresar(interes)


class CuentaCorriente(Cuenta):
    def __init__(self, cliente: Cliente, limite_descubierto: float = 0.0):
        super().__init__(cliente)
        self.__limite_descubierto = float(limite_descubierto)

    def retirar(self, monto: float) -> Transaccion:
        if monto <= 0:
            raise ValueError("El monto a retirar debe ser mayor que cero")
        disponible = self.saldo + self.__limite_descubierto
        if monto > disponible:
            raise ValueError("Saldo + límite insuficiente")
        # permitir saldo negativo hasta el límite
        # ajustar saldo directamente (no usar super para evitar la comprobación estricta)
        # nota: accesamos el atributo privado mediante el getter/modificación indirecta
        # aquí, para mantener encapsulamiento, usamos la lógica de la clase padre a través de manipulación controlada
        # pero en python, no hay acceso directo a __saldo desde aquí, así usaremos los métodos públicos:
        # retirar parcialmente del saldo si suficiente, o dejar saldo negativo
        if monto <= self.saldo:
            return super().retirar(monto)
        else:
            # monto mayor que saldo pero <= saldo+limite
            # restar todo el saldo y dejar negativo
            exceso = monto - self.saldo
            # vaciar saldo
            # hack: usar internal name mangling to set private saldo
            # _Cuenta__saldo es nombre mangled
            try:
                current = getattr(self, "_Cuenta__saldo")
                setattr(self, "_Cuenta__saldo", current - monto)
                tx = Transaccion("RET", monto)
                getattr(self, "_Cuenta__transacciones").append(tx)
                return tx
            except Exception as e:
                raise RuntimeError("Error interno al procesar retiro con descubierto") from e


# ---------- ALMACENAMIENTO EN MEMORIA ----------
class Banco:
    def __init__(self):
        self._clientes: List[Cliente] = []
        self._cuentas: List[Cuenta] = []

    # Cliente CRUD
    def crear_cliente(self, nombre: str, apellido: str, dni: str) -> Cliente:
        if self.buscar_cliente_por_dni(dni) is not None:
            raise ValueError("Ya existe un cliente con ese DNI")
        cliente = Cliente(nombre, apellido, dni)
        self._clientes.append(cliente)
        return cliente

    def buscar_cliente_por_dni(self, dni: str) -> Optional[Cliente]:
        for c in self._clientes:
            if c.dni == dni:
                return c
        return None

    def listar_clientes(self) -> List[Cliente]:
        return list(self._clientes)

    # Cuentas
    def crear_cuenta_ahorro(self, dni_cliente: str, tasa_interes: float = 0.01) -> CuentaAhorro:
        cliente = self.buscar_cliente_por_dni(dni_cliente)
        if cliente is None:
            raise ValueError("Cliente no encontrado")
        cuenta = CuentaAhorro(cliente, tasa_interes)
        self._cuentas.append(cuenta)
        return cuenta

    def crear_cuenta_corriente(self, dni_cliente: str, limite_descubierto: float = 0.0) -> CuentaCorriente:
        cliente = self.buscar_cliente_por_dni(dni_cliente)
        if cliente is None:
            raise ValueError("Cliente no encontrado")
        cuenta = CuentaCorriente(cliente, limite_descubierto)
        self._cuentas.append(cuenta)
        return cuenta

    def buscar_cuenta_por_num(self, numero: str) -> Optional[Cuenta]:
        for c in self._cuentas:
            if c.numero_cuenta == numero:
                return c
        return None

    def listar_cuentas(self) -> List[Cuenta]:
        return list(self._cuentas)


# ---------- GENERADOR DE PDF (FPDF) ----------
try:
    from fpdf import FPDF
except Exception:
    FPDF = None

class PDFGenerator:
    def __init__(self, filename: str = "reporte.pdf"):
        if FPDF is None:
            raise ImportError("FPDF no está instalado. Ejecutar: pip install fpdf2")
        self.filename = filename

    def generar_pdf_cliente(self, cliente: Cliente, cuentas: List[Cuenta]):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"Reporte Cliente: {cliente.nombre} {cliente.apellido}", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 8, f"DNI: {cliente.dni}", ln=True)
        pdf.ln(6)
        for cuenta in cuentas:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, f"Cuenta: {cuenta.numero_cuenta}", ln=True)
            pdf.set_font("Arial", size=11)
            pdf.cell(0, 8, f"Saldo: {cuenta.saldo}", ln=True)
            pdf.cell(0, 6, "Transacciones:", ln=True)
            for tx in cuenta.obtener_transacciones()[-10:]:
                pdf.cell(0, 6, f" - {tx.fecha.strftime('%Y-%m-%d %H:%M:%S')} {tx.tipo} {tx.monto}", ln=True)
            pdf.ln(4)
        pdf.cell(0, 6, f"Generado: {datetime.now().isoformat()}")
        pdf.output(self.filename)
        return self.filename


# ---------- INTERFAZ GRÁFICA BÁSICA CON FLET ----------
try:
    import flet as ft
except Exception:
    ft = None


def run_flet_app(banco: Banco):
    if ft is None:
        raise ImportError("Flet no está instalado. Ejecutar: pip install flet")

    def main(page: ft.Page):
        page.title = "Sistema Bancario - TP"
        page.padding = 20

        # Inputs cliente
        nombre = ft.TextField(label="Nombre", width=300)
        apellido = ft.TextField(label="Apellido", width=300)
        dni = ft.TextField(label="DNI", width=300)

        # Mensajes y lista
        mensajes = ft.Text(value="", selectable=True)
        cuentas_list = ft.ListView(expand=True, spacing=5)

        def mostrar_clientes(_=None):
            cuentas_list.controls.clear()
            for c in banco.listar_clientes():
                cuentas_list.controls.append(ft.Text(str(c)))
            page.update()

        def crear_cliente_click(e):
            try:
                cliente = banco.crear_cliente(nombre.value, apellido.value, dni.value)
                mensajes.value = f"Cliente creado: {cliente}"
                nombre.value = apellido.value = dni.value = ""
                mostrar_clientes()
            except Exception as ex:
                mensajes.value = f"Error: {ex}"
                print(traceback.format_exc())
            page.update()

        # Operaciones de cuenta
        dni_buscar = ft.TextField(label="DNI cliente (buscar)", width=300)
        tipo_cuenta = ft.Dropdown(options=[ft.dropdown.Option("Ahorro"), ft.dropdown.Option("Corriente")], value="Ahorro")
        crear_cuenta_btn = ft.ElevatedButton(text="Crear cuenta", on_click=lambda e: crear_cuenta(e))

        def crear_cuenta(e):
            try:
                d = dni_buscar.value
                if tipo_cuenta.value == "Ahorro":
                    cuenta = banco.crear_cuenta_ahorro(d)
                else:
                    cuenta = banco.crear_cuenta_corriente(d, limite_descubierto=1000.0)
                mensajes.value = f"Cuenta creada: {cuenta.numero_cuenta} para cliente {cuenta.cliente}"
                mostrar_cuentas_por_cliente(d)
            except Exception as ex:
                mensajes.value = f"Error: {ex}"
                print(traceback.format_exc())
            page.update()

        def mostrar_cuentas_por_cliente(dni_val: str):
            cuentas_list.controls.clear()
            for c in banco.listar_cuentas():
                if c.cliente.dni == dni_val:
                    cuentas_list.controls.append(ft.Text(f"{c.numero_cuenta} - Saldo: {c.saldo}"))
            page.update()

        # Operaciones de depósito / retiro
        nro_cuenta_field = ft.TextField(label="Nro de cuenta", width=300)
        monto_field = ft.TextField(label="Monto", width=300)

        def operar(e, tipo: str):
            try:
                cuenta = banco.buscar_cuenta_por_num(nro_cuenta_field.value)
                if cuenta is None:
                    raise ValueError("Cuenta no encontrada")
                monto = float(monto_field.value)
                if tipo == "DEP":
                    tx = cuenta.ingresar(monto)
                else:
                    tx = cuenta.retirar(monto)
                mensajes.value = f"Operación OK: {tx} - Nuevo saldo: {cuenta.saldo}"
            except Exception as ex:
                mensajes.value = f"Error: {ex}"
                print(traceback.format_exc())
            page.update()

        btn_depositar = ft.ElevatedButton(text="Depositar", on_click=lambda e: operar(e, "DEP"))
        btn_retirar = ft.ElevatedButton(text="Retirar", on_click=lambda e: operar(e, "RET"))

        # Generar PDF
        nombre_pdf = ft.TextField(label="Nombre archivo PDF", width=300, value="reporte_cliente.pdf")
        def generar_pdf_click(e):
            try:
                dni_v = dni_buscar.value
                cliente = banco.buscar_cliente_por_dni(dni_v)
                if cliente is None:
                    raise ValueError("Cliente no encontrado")
                cuentas = [c for c in banco.listar_cuentas() if c.cliente.dni == dni_v]
                pdf_gen = PDFGenerator(nombre_pdf.value)
                file_path = pdf_gen.generar_pdf_cliente(cliente, cuentas)
                mensajes.value = f"PDF generado: {file_path}"
            except Exception as ex:
                mensajes.value = f"Error: {ex}"
                print(traceback.format_exc())
            page.update()

        btn_pdf = ft.ElevatedButton(text="Generar PDF", on_click=generar_pdf_click)

        # Layout
        controls = [
            ft.Row([ft.Column([ft.Text("Crear Cliente", style=ft.TextStyle(size=16)), nombre, apellido, dni, ft.ElevatedButton(text="Crear", on_click=crear_cliente_click)]) , ft.Column([ft.Text("Clientes existentes", style=ft.TextStyle(size=16)), cuentas_list])]),
            ft.Divider(),
            ft.Row([ft.Column([ft.Text("Operaciones de Cuenta", style=ft.TextStyle(size=14)), dni_buscar, tipo_cuenta, crear_cuenta_btn, nombre_pdf, btn_pdf]), ft.Column([ft.Text("Operar en cuenta", style=ft.TextStyle(size=14)), nro_cuenta_field, monto_field, ft.Row([btn_depositar, btn_retirar])])]),
            ft.Divider(),
            mensajes
        ]

        page.add(*controls)
        mostrar_clientes()

    ft.app(target=main, view=ft.WEB_BROWSER, assets_dir="assets")


# Si se ejecuta como script, iniciar banco y UI
if __name__ == "__main__":
    banco = Banco()
    # pre-cargar datos de ejemplo (opcional)
    try:
        c1 = banco.crear_cliente("Rocio", "Jacob", "12345678")
        cuenta = banco.crear_cuenta_ahorro(c1.dni, tasa_interes=0.02)
        cuenta.ingresar(1000)
    except Exception:
        pass

    # Ejecuta la app Flet si está disponible;
    # si no, simplemente muestra instrucciones
    if ft is not None:
        try:
            run_flet_app(banco)
        except Exception as e:
            print("Error lanzando la UI:", e)
            print(traceback.format_exc())
    else:
        print("Flet no instalado. Para ejecutar la UI instalar flet y volver a correr el script.")


# ---------- Nota sobre pruebas (pytest) ----------
# Recomendación: crear archivo tests/test_models.py con tests como:
#
# def test_crear_cliente_valido():
#     c = Cliente('A','B','123')
#     assert c.nombre == 'A'
#
# def test_ingresar_retirar():
#     c = Cliente('A','B','111')
#     cu = CuentaAhorro(c)
#     cu.ingresar(100)
#     with pytest.raises(ValueError):
#         cu.retirar(200)
#
# Ejecutar: pytest -q
