import flet as ft
import datetime
from almacenamiento import Banco
from reporte_pdf import PDFGenerator


class ClienteDetailView:
    """Vista de detalle del cliente con sus cuentas"""

    def __init__(self, page: ft.Page, banco: Banco, dni_cliente: str, on_navigate):
        self.page = page
        self.banco = banco
        self.dni_cliente = dni_cliente
        self.on_navigate = on_navigate
        self.cliente = banco.buscar_cliente_por_dni(dni_cliente)

        if not self.cliente:
            raise ValueError("Cliente no encontrado")

        # Obtener cuentas
        self.cuentas = banco.listar_cuentas_por_cliente(dni_cliente)
        self.cuenta_ahorro = None
        self.cuenta_corriente = None
        for cuenta in self.cuentas:
            if cuenta.__class__.__name__ == "CuentaAhorro":
                self.cuenta_ahorro = cuenta
            elif cuenta.__class__.__name__ == "CuentaCorriente":
                self.cuenta_corriente = cuenta

        self.mensaje = ft.Text(value="", color=ft.Colors.RED_700)

        # contenedores que se actualizarán sin recargar
        self.card_ahorro_container = ft.Container()
        self.card_corriente_container = ft.Container()

    def volver_listado(self, e):
        self.on_navigate("listado")

    # ---- CREAR CUENTAS ----
    def crear_cuenta(self, e, tipo: str):
        """Crea una cuenta y actualiza la card sin recargar"""
        try:
            if tipo == "ahorro":
                self.cuenta_ahorro = self.banco.crear_cuenta_ahorro(self.dni_cliente, tasa_interes=0.02)
                self.mensaje.value = "✅ Caja de Ahorro creada exitosamente"
            else:
                self.cuenta_corriente = self.banco.crear_cuenta_corriente(self.dni_cliente, limite_descubierto=1000.0)
                self.mensaje.value = "✅ Cuenta Corriente creada exitosamente"

            self.mensaje.color = ft.Colors.GREEN_700
            # Actualizamos solo las cards, no toda la página
            self.actualizar_cards()
            self.page.update()

        except Exception as ex:
            self.mensaje.value = f"❌ Error: {ex}"
            self.mensaje.color = ft.Colors.RED_700
            self.page.update()

    # ---- OPERAR CUENTA ----
    def operar_cuenta(self, e, cuenta, tipo_operacion: str, monto_input, tabla_transacciones, saldo_text):
        """Opera sobre la cuenta (ingresar/retirar) y actualiza datos en vivo"""
        try:
            monto = float(monto_input.value)
            if monto <= 0:
                raise ValueError("El monto debe ser mayor que 0")

            if tipo_operacion == "ingresar":
                cuenta.ingresar(monto)
                self.mensaje.value = f"✅ Depósito exitoso: ${monto:.2f}"
            else:
                cuenta.retirar(monto)
                self.mensaje.value = f"✅ Retiro exitoso: ${monto:.2f}"

            self.mensaje.color = ft.Colors.GREEN_700
            monto_input.value = ""

            # actualizar saldo y tabla
            saldo_text.value = f"Saldo: ${cuenta.saldo:.2f}"
            saldo_text.color = ft.Colors.GREEN_700 if cuenta.saldo >= 0 else ft.Colors.RED_700
            self.actualizar_tabla_transacciones(tabla_transacciones, cuenta)

            self.page.update()

        except Exception as ex:
            self.mensaje.value = f"❌ Error: {ex}"
            self.mensaje.color = ft.Colors.RED_700
            self.page.update()

    # ---- TABLA ----
    def actualizar_tabla_transacciones(self, tabla: ft.DataTable, cuenta):
        tabla.rows.clear()
        transacciones = cuenta.obtener_transacciones()

        if not transacciones:
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Container(
                                ft.Text("Sin transacciones", italic=True, color=ft.Colors.GREY_600, size=12),
                                padding=ft.padding.symmetric(vertical=4, horizontal=8),
                                alignment=ft.alignment.center_left,
                                expand=True,
                            )
                        ),
                        ft.DataCell(ft.Container()),  # celda vacía
                        ft.DataCell(ft.Container()),  # celda vacía
                    ]
                )
            )
        else:
            for tx in transacciones[-10:]:
                color = ft.Colors.GREEN_700 if tx.tipo == "DEP" else ft.Colors.RED_700
                tabla.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Container(
                                    ft.Text(tx.fecha.strftime("%d/%m/%Y %H:%M"), size=12),
                                    padding=ft.padding.symmetric(vertical=4, horizontal=8),
                                    alignment=ft.alignment.center_left,
                                    expand=True,
                                )
                            ),
                            ft.DataCell(
                                ft.Container(
                                    ft.Text(tx.tipo, color=color, weight=ft.FontWeight.BOLD, size=12),
                                    padding=ft.padding.symmetric(vertical=4, horizontal=8),
                                    alignment=ft.alignment.center_left,
                                    expand=True,
                                )
                            ),
                            ft.DataCell(
                                ft.Container(
                                    ft.Text(f"${tx.monto:.2f}", color=color, size=12),
                                    padding=ft.padding.symmetric(vertical=4, horizontal=8),
                                    alignment=ft.alignment.center_left,
                                    expand=True,
                                )
                            ),
                        ]
                    )
                )

    # ---- PDF ----
    def generar_pdf(self, e):
        try:
            pdf_gen = PDFGenerator(f"cliente_{self.dni_cliente}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")
            archivo = pdf_gen.generar_pdf_cliente(self.cliente, self.cuentas)
            self.mensaje.value = f"✅ PDF generado: {archivo}"
            self.mensaje.color = ft.Colors.GREEN_700
            self.page.update()
        except Exception as ex:
            self.mensaje.value = f"❌ Error al generar PDF: {ex}"
            self.mensaje.color = ft.Colors.RED_700
            self.page.update()

    # ---- RENDERIZADO DE CARD ----
    def render_cuenta_card(self, titulo: str, cuenta, tipo: str):
        if cuenta is None:
            return ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, size=50, color=ft.Colors.GREY_400),
                        ft.Text(titulo, size=18, weight=ft.FontWeight.BOLD),
                        ft.Text("No tiene cuenta creada", color=ft.Colors.GREY_600),
                        ft.Container(height=10),
                        ft.ElevatedButton(
                            f"Crear {titulo}",
                            icon=ft.Icons.ADD,
                            on_click=lambda e: self.crear_cuenta(e, tipo)
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=30,
                    alignment=ft.alignment.center,
                ),
                elevation=2,
            )

        # Si tiene cuenta
        monto_input = ft.TextField(label="Monto", width=200, height=35, content_padding=ft.padding.all(5), keyboard_type=ft.KeyboardType.NUMBER)
        saldo_text = ft.Text(f"Saldo: ${cuenta.saldo:.2f}", size=18, weight=ft.FontWeight.BOLD,
                             color=ft.Colors.GREEN_700 if cuenta.saldo >= 0 else ft.Colors.RED_700)

        tabla_transacciones = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Fecha", size=12, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Tipo", size=12, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Monto", size=12, weight=ft.FontWeight.BOLD)),
            ],
            heading_row_height=32,
            data_row_min_height=32,
            data_row_max_height=36,
            column_spacing=6,
            border=ft.border.all(1, ft.Colors.GREY_400),
            vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_300),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_300),
            border_radius=5,
        )

        self.actualizar_tabla_transacciones(tabla_transacciones, cuenta)

        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, size=30, color=ft.Colors.BLUE_700),
                        ft.Text(titulo, size=18, weight=ft.FontWeight.BOLD),
                    ]),
                    ft.Divider(),

                    ft.Container(
                        content=ft.Column([
                            ft.Text(f"Número: {cuenta.numero_cuenta}", size=14),
                            saldo_text,
                        ]),
                        bgcolor=ft.Colors.BLUE_50,
                        padding=10,
                        border_radius=8,
                    ),

                    ft.Container(height=10),
                    ft.Text("Operaciones", size=16, weight=ft.FontWeight.BOLD),
                    monto_input,
                    ft.Row([
                        ft.ElevatedButton(
                            "Ingresar",
                            icon=ft.Icons.ARROW_DOWNWARD,
                            bgcolor=ft.Colors.GREEN_700,
                            color=ft.Colors.WHITE,
                            on_click=lambda e: self.operar_cuenta(e, cuenta, "ingresar", monto_input, tabla_transacciones, saldo_text)
                        ),
                        ft.ElevatedButton(
                            "Retirar",
                            icon=ft.Icons.ARROW_UPWARD,
                            bgcolor=ft.Colors.RED_700,
                            color=ft.Colors.WHITE,
                            on_click=lambda e: self.operar_cuenta(e, cuenta, "retirar", monto_input, tabla_transacciones, saldo_text)
                        ),
                    ]),
                    ft.Divider(),
                    ft.Text("Historial de Transacciones", size=16, weight=ft.FontWeight.BOLD),
                    ft.Container(content=tabla_transacciones, height=250),
                ]),
                padding=20,
            ),
            elevation=2,
        )

    # ---- ACTUALIZACIÓN DE LAS CARDS ----
    def actualizar_cards(self):
        self.card_ahorro_container.content = self.render_cuenta_card("Caja de Ahorro", self.cuenta_ahorro, "ahorro")
        self.card_corriente_container.content = self.render_cuenta_card("Cuenta Corriente", self.cuenta_corriente, "corriente")

    # ---- RENDER PRINCIPAL ----
    def render(self):
        self.actualizar_cards()
        return ft.Column(
            controls=[
                ft.Row([
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Volver al listado", on_click=self.volver_listado),
                    ft.Text("Detalle del Cliente", size=26, weight=ft.FontWeight.BOLD),
                ]),
                ft.Divider(),

                ft.Card(
                    content=ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.PERSON, size=50, color=ft.Colors.BLUE_700),
                            ft.Column([
                                ft.Text(f"{self.cliente.nombre} {self.cliente.apellido}", size=22, weight=ft.FontWeight.BOLD),
                                ft.Text(f"DNI: {self.cliente.dni}", size=14),
                            ]),
                            ft.Container(expand=True),
                            ft.ElevatedButton("Generar PDF", icon=ft.Icons.PICTURE_AS_PDF, on_click=self.generar_pdf),
                        ]),
                        padding=15,
                    ),
                    elevation=2,
                ),

                self.mensaje,
                ft.Container(height=10),

                ft.Text("Cuentas del Cliente", size=20, weight=ft.FontWeight.BOLD),
                ft.Row(
                    controls=[
                        self.card_ahorro_container,
                        self.card_corriente_container,
                    ],
                    spacing=20,
                ),
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        )
