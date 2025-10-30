import traceback
from almacenamiento import Banco 
from reporte_pdf import PDFGenerator 
# Importación de modelos
from cliente import Cliente 
from cuenta import Cuenta 

try:
    import flet as ft
except Exception:
    ft = None
# ... (el resto de la función run_flet_app(banco) es el mismo) ...

# ... (Todo el código de la UI es el mismo, solo las importaciones cambian) ...

def run_flet_app(banco: Banco):
    if ft is None:
        raise ImportError("Flet no está instalado. Ejecutar: pip install flet")

    def main(page: ft.Page):
        # ... (Toda la implementación de la UI) ...
        page.title = "Sistema Bancario - TP"
        page.padding = 20
        # Inputs cliente ...
        nombre = ft.TextField(label="Nombre", width=250)
        apellido = ft.TextField(label="Apellido", width=250)
        dni = ft.TextField(label="DNI", width=250)
        # Mensajes y lista ...
        mensajes = ft.Text(value="", selectable=True, color=ft.Colors.RED_700)
        cuentas_list = ft.ListView(expand=True, spacing=5, auto_scroll=True)
        clientes_list = ft.Column(scroll=ft.ScrollMode.ADAPTIVE, expand=True)

        def mostrar_clientes_en_ui(_=None):
            clientes_list.controls.clear()
            for c in banco.listar_clientes():
                clientes_list.controls.append(ft.Text(str(c)))
            page.update()

        def crear_cliente_click(e):
            try:
                cliente = banco.crear_cliente(nombre.value, apellido.value, dni.value)
                mensajes.value = f"✅ Cliente creado: {cliente}"
                nombre.value = apellido.value = dni.value = ""
                mostrar_clientes_en_ui()
            except Exception as ex:
                mensajes.value = f"❌ Error al crear cliente: {ex}"
                print(traceback.format_exc())
            page.update()

        # Operaciones de cuenta ...
        dni_buscar = ft.TextField(label="DNI cliente (buscar/crear cuenta)", width=300)
        tipo_cuenta = ft.Dropdown(options=[ft.dropdown.Option("Ahorro"), ft.dropdown.Option("Corriente")], value="Ahorro", width=300)
        limite_descubierto_field = ft.TextField(label="Límite Descubierto (solo Cta. Cte)", value="1000.0", width=300)
        crear_cuenta_btn = ft.ElevatedButton(text="Crear cuenta", on_click=lambda e: crear_cuenta(e))
        
        def mostrar_cuentas_por_cliente(dni_val: str):
            cuentas_list.controls.clear()
            cuentas_cliente = banco.listar_cuentas_por_cliente(dni_val)
            if not cuentas_cliente:
                 cuentas_list.controls.append(ft.Text(f"No hay cuentas para DNI: {dni_val}"))

            for c in cuentas_cliente:
                btn_detalles = ft.TextButton(text="Detalles/Transacciones", 
                                             on_click=lambda e, cuenta_num=c.numero_cuenta: mostrar_transacciones(e, cuenta_num))
                cuentas_list.controls.append(ft.Container(
                    content=ft.Row([
                        ft.Text(f"Num: {c.numero_cuenta} - Saldo: {c.saldo:.2f} ({c.__class__.__name__})"),
                        btn_detalles
                    ]),
                    padding=5, border=ft.border.all(1, ft.Colors.BLACK12)
                ))
            page.update()

        def crear_cuenta(e):
            try:
                d = dni_buscar.value
                limite = float(limite_descubierto_field.value) if limite_descubierto_field.value else 0.0
                if tipo_cuenta.value == "Ahorro":
                    cuenta = banco.crear_cuenta_ahorro(d)
                else:
                    cuenta = banco.crear_cuenta_corriente(d, limite_descubierto=limite)
                mensajes.value = f"✅ Cuenta creada: {cuenta.numero_cuenta} ({cuenta.__class__.__name__})"
                mostrar_cuentas_por_cliente(d)
            except Exception as ex:
                mensajes.value = f"❌ Error al crear cuenta: {ex}"
                print(traceback.format_exc())
            page.update()

        # Operaciones de depósito / retiro
        nro_cuenta_field = ft.TextField(label="Nro de cuenta (operar)", width=300)
        monto_field = ft.TextField(label="Monto (operar)", width=300)

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
                mensajes.value = f"✅ Operación {tipo} OK: {tx.monto:.2f} - Nuevo saldo: {cuenta.saldo:.2f}"
                mostrar_cuentas_por_cliente(cuenta.cliente.dni)
            except Exception as ex:
                mensajes.value = f"❌ Error en operación: {ex}"
                print(traceback.format_exc())
            page.update()

        btn_depositar = ft.ElevatedButton(text="Depositar", on_click=lambda e: operar(e, "DEP"))
        btn_retirar = ft.ElevatedButton(text="Retirar", on_click=lambda e: operar(e, "RET"))
        
        # Mostrar transacciones en un diálogo
        def mostrar_transacciones(e, numero_cuenta: str):
            cuenta = banco.buscar_cuenta_por_num(numero_cuenta)
            if cuenta is None: return

            transacciones_content = ft.Column(scroll=ft.ScrollMode.ADAPTIVE)
            transacciones = cuenta.obtener_transacciones()
            
            transacciones_content.controls.append(ft.Text(f"Transacciones de Cuenta: {numero_cuenta}", weight=ft.FontWeight.BOLD))

            if not transacciones:
                transacciones_content.controls.append(ft.Text("No hay transacciones registradas."))
            else:
                for tx in transacciones:
                    color = ft.Colors.GREEN_700 if tx.tipo == "DEP" else ft.Colors.RED_700
                    transacciones_content.controls.append(
                        ft.Text(f"{tx.fecha.strftime('%Y-%m-%d %H:%M:%S')} | {tx.tipo} | {tx.monto:.2f}", color=color)
                    )

            dialog = ft.AlertDialog(
                title=ft.Text("Historial de Transacciones"),
                content=ft.Container(content=transacciones_content, height=400, width=400),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: close_dialog(e, dialog)),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.dialog = dialog
            dialog.open = True
            page.update()

        def close_dialog(e, dialog):
            dialog.open = False
            page.update()
        
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
                mensajes.value = f"✅ PDF generado: {file_path}"
            except ImportError:
                 mensajes.value = f"❌ Error: {traceback.format_exc().splitlines()[-1].strip()}. Debe instalar fpdf2."
            except Exception as ex:
                mensajes.value = f"❌ Error al generar PDF: {ex}"
                print(traceback.format_exc())
            page.update()

        btn_pdf = ft.ElevatedButton(text="Generar PDF", on_click=generar_pdf_click)

        # Layout Tabs
        tab_clientes = ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text("Crear Cliente", weight=ft.FontWeight.BOLD, size=16), 
                    nombre, apellido, dni, 
                    ft.ElevatedButton(text="Crear Cliente", on_click=crear_cliente_click)
                ], expand=True), 
                ft.VerticalDivider(),
                ft.Column([
                    ft.Text("Clientes Existentes", weight=ft.FontWeight.BOLD, size=16), 
                    clientes_list
                ], expand=True)
            ], expand=True),
        ])

        tab_cuentas = ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text("Gestión de Cuentas", weight=ft.FontWeight.BOLD, size=16), 
                    dni_buscar, 
                    tipo_cuenta,
                    limite_descubierto_field,
                    crear_cuenta_btn,
                    ft.Text("Reporte PDF", weight=ft.FontWeight.BOLD, size=14),
                    nombre_pdf,
                    btn_pdf,
                    ft.Divider(height=10),
                    ft.ElevatedButton(text="Buscar Cuentas (por DNI)", on_click=lambda e: mostrar_cuentas_por_cliente(dni_buscar.value))
                ], expand=True),
                ft.VerticalDivider(),
                ft.Column([
                    ft.Text("Operar en Cuenta", weight=ft.FontWeight.BOLD, size=16),
                    nro_cuenta_field, 
                    monto_field, 
                    ft.Row([btn_depositar, btn_retirar]),
                    ft.Divider(height=10),
                    ft.Text("Cuentas del Cliente Seleccionado", weight=ft.FontWeight.BOLD, size=14),
                    cuentas_list
                ], expand=True),
            ], expand=True),
        ], expand=True)

        t = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            expand=1,
            tabs=[
                ft.Tab(
                    text="Clientes",
                    icon=ft.Icons.PEOPLE,
                    content=tab_clientes,
                ),
                ft.Tab(
                    text="Cuentas & Operaciones",
                    icon=ft.Icons.ACCOUNT_BALANCE,
                    content=tab_cuentas,
                ),
            ],
        )

        page.add(t, ft.Divider(height=5), mensajes)
        mostrar_clientes_en_ui() # Cargar clientes al inicio


    ft.app(target=main, view=ft.WEB_BROWSER)