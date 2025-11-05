import flet as ft
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
        
        # Obtener cuentas del cliente
        self.cuentas = banco.listar_cuentas_por_cliente(dni_cliente)
        self.cuenta_ahorro = None
        self.cuenta_corriente = None
        
        for cuenta in self.cuentas:
            if cuenta.__class__.__name__ == "CuentaAhorro":
                self.cuenta_ahorro = cuenta
            elif cuenta.__class__.__name__ == "CuentaCorriente":
                self.cuenta_corriente = cuenta
        
        self.mensaje = ft.Text(value="", color=ft.Colors.RED_700)
    
    def volver_listado(self, e):
        """Vuelve al listado de clientes"""
        self.on_navigate("listado")
    
    def crear_cuenta(self, e, tipo: str):
        """Crea una cuenta del tipo especificado"""
        try:
            if tipo == "ahorro":
                cuenta = self.banco.crear_cuenta_ahorro(self.dni_cliente, tasa_interes=0.02)
                self.cuenta_ahorro = cuenta
                self.mensaje.value = "✅ Caja de Ahorro creada exitosamente"
            else:
                cuenta = self.banco.crear_cuenta_corriente(self.dni_cliente, limite_descubierto=1000.0)
                self.cuenta_corriente = cuenta
                self.mensaje.value = "✅ Cuenta Corriente creada exitosamente"
            
            self.mensaje.color = ft.Colors.GREEN_700
            self.page.go(f"/detalle/{self.dni_cliente}")  # Recargar vista
            
        except Exception as ex:
            self.mensaje.value = f"❌ Error: {ex}"
            self.mensaje.color = ft.Colors.RED_700
            self.page.update()
    
    def operar_cuenta(self, e, cuenta, tipo_operacion: str, monto_input: ft.TextField):
        """Realiza una operación en la cuenta"""
        try:
            monto = float(monto_input.value)
            
            if tipo_operacion == "ingresar":
                cuenta.ingresar(monto)
                self.mensaje.value = f"✅ Depósito exitoso: ${monto:.2f}"
            else:
                cuenta.retirar(monto)
                self.mensaje.value = f"✅ Retiro exitoso: ${monto:.2f}"
            
            self.mensaje.color = ft.Colors.GREEN_700
            monto_input.value = ""
            self.page.go(f"/detalle/{self.dni_cliente}")  # Recargar vista
            
        except Exception as ex:
            self.mensaje.value = f"❌ Error: {ex}"
            self.mensaje.color = ft.Colors.RED_700
            self.page.update()
    
    def generar_pdf(self, e):
        """Genera el PDF del cliente"""
        try:
            pdf_gen = PDFGenerator(f"cliente_{self.dni_cliente}.pdf")
            archivo = pdf_gen.generar_pdf_cliente(self.cliente, self.cuentas)
            self.mensaje.value = f"✅ PDF generado: {archivo}"
            self.mensaje.color = ft.Colors.GREEN_700
            self.page.update()
        except Exception as ex:
            self.mensaje.value = f"❌ Error al generar PDF: {ex}"
            self.mensaje.color = ft.Colors.RED_700
            self.page.update()
    
    def render_cuenta_card(self, titulo: str, cuenta, tipo: str):
        """Renderiza una card de cuenta (ahorro o corriente)"""
        
        if cuenta is None:
            # No tiene cuenta - mostrar botón para crear
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
        
        # Tiene cuenta - mostrar detalles y operaciones
        monto_input = ft.TextField(label="Monto", width=200, keyboard_type=ft.KeyboardType.NUMBER)
        
        # Tabla de transacciones
        tabla_transacciones = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Tipo")),
                ft.DataColumn(ft.Text("Monto")),
            ],
            rows=[],
            heading_row_height=40,
            data_row_max_height=40,
        )
        
        transacciones = cuenta.obtener_transacciones()
        for tx in transacciones[-10:]:  # Últimas 10
            color = ft.Colors.GREEN_700 if tx.tipo == "DEP" else ft.Colors.RED_700
            tabla_transacciones.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(tx.fecha.strftime("%d/%m/%Y %H:%M"))),
                        ft.DataCell(ft.Text(tx.tipo, color=color, weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(f"${tx.monto:.2f}", color=color)),
                    ]
                )
            )
        
        if not transacciones:
            tabla_transacciones.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Sin transacciones", italic=True, color=ft.Colors.GREY_600, colspan=3))
                    ]
                )
            )
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, size=30, color=ft.Colors.BLUE_700),
                        ft.Text(titulo, size=18, weight=ft.FontWeight.BOLD),
                    ]),
                    ft.Divider(),
                    
                    # Info de la cuenta
                    ft.Container(
                        content=ft.Column([
                            ft.Text(f"Número: {cuenta.numero_cuenta}", size=14),
                            ft.Text(f"Saldo: ${cuenta.saldo:.2f}", 
                                  size=24, 
                                  weight=ft.FontWeight.BOLD,
                                  color=ft.Colors.GREEN_700 if cuenta.saldo >= 0 else ft.Colors.RED_700),
                        ]),
                        bgcolor=ft.Colors.BLUE_50,
                        padding=15,
                        border_radius=10,
                    ),
                    
                    ft.Container(height=10),
                    
                    # Operaciones
                    ft.Text("Operaciones", size=16, weight=ft.FontWeight.BOLD),
                    monto_input,
                    ft.Row([
                        ft.ElevatedButton(
                            "Ingresar Dinero",
                            icon=ft.Icons.ARROW_DOWNWARD,
                            bgcolor=ft.Colors.GREEN_700,
                            color=ft.Colors.WHITE,
                            on_click=lambda e: self.operar_cuenta(e, cuenta, "ingresar", monto_input)
                        ),
                        ft.ElevatedButton(
                            "Retirar Dinero",
                            icon=ft.Icons.ARROW_UPWARD,
                            bgcolor=ft.Colors.RED_700,
                            color=ft.Colors.WHITE,
                            on_click=lambda e: self.operar_cuenta(e, cuenta, "retirar", monto_input)
                        ),
                    ]),
                    
                    ft.Container(height=10),
                    ft.Divider(),
                    
                    # Historial
                    ft.Text("Historial de Transacciones", size=16, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=tabla_transacciones,
                        height=250,
                    ),
                ]),
                padding=20,
            ),
            elevation=2,
        )
    
    def render(self):
        """Renderiza la vista completa"""
        return ft.Column(
            controls=[
                # Botón volver
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        tooltip="Volver al listado",
                        on_click=self.volver_listado
                    ),
                    ft.Text("Detalle del Cliente", size=28, weight=ft.FontWeight.BOLD),
                ]),
                
                ft.Divider(),
                
                # Info del cliente
                ft.Card(
                    content=ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.PERSON, size=50, color=ft.Colors.BLUE_700),
                            ft.Column([
                                ft.Text(f"{self.cliente.nombre} {self.cliente.apellido}", 
                                      size=24, weight=ft.FontWeight.BOLD),
                                ft.Text(f"DNI: {self.cliente.dni}", size=16),
                            ]),
                            ft.Container(expand=True),
                            ft.ElevatedButton(
                                "Generar PDF",
                                icon=ft.Icons.PICTURE_AS_PDF,
                                on_click=self.generar_pdf
                            ),
                        ]),
                        padding=20,
                    ),
                    elevation=2,
                ),
                
                self.mensaje,
                
                ft.Container(height=10),
                
                # Cuentas en 2 columnas
                ft.Text("Cuentas del Cliente", size=20, weight=ft.FontWeight.BOLD),
                ft.Row(
                    controls=[
                        ft.Container(
                            content=self.render_cuenta_card("Caja de Ahorro", self.cuenta_ahorro, "ahorro"),
                            expand=True,
                        ),
                        ft.Container(
                            content=self.render_cuenta_card("Cuenta Corriente", self.cuenta_corriente, "corriente"),
                            expand=True,
                        ),
                    ],
                    spacing=20,
                ),
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        )
