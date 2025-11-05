import flet as ft
from almacenamiento import Banco

class ClienteListView:
    """Vista del listado de clientes en tabla"""
    
    def __init__(self, page: ft.Page, banco: Banco, on_navigate):
        self.page = page
        self.banco = banco
        self.on_navigate = on_navigate
        self.mensaje = ft.Text(value="", color=ft.Colors.RED_700)
        
        # Campos del formulario
        self.nombre_input = ft.TextField(label="Nombre", width=200)
        self.apellido_input = ft.TextField(label="Apellido", width=200)
        self.dni_input = ft.TextField(label="DNI", width=150)
        
        # Tabla de clientes
        self.tabla_clientes = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("DNI", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Nombre", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Apellido", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Acciones", weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_300),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_300),
        )
    
    def crear_cliente(self, e):
        """Crea un nuevo cliente"""
        try:
            cliente = self.banco.crear_cliente(
                self.nombre_input.value,
                self.apellido_input.value,
                self.dni_input.value
            )
            self.mensaje.value = f"✅ Cliente creado: {cliente.nombre} {cliente.apellido}"
            self.mensaje.color = ft.Colors.GREEN_700
            
            # Limpiar campos
            self.nombre_input.value = ""
            self.apellido_input.value = ""
            self.dni_input.value = ""
            
            # Actualizar tabla
            self.actualizar_tabla()
            self.page.update()
            
        except Exception as ex:
            self.mensaje.value = f"❌ Error: {ex}"
            self.mensaje.color = ft.Colors.RED_700
            self.page.update()
    
    def ver_detalle_cliente(self, dni: str):
        """Navega al detalle del cliente"""
        self.on_navigate("detalle", dni)
    
    def actualizar_tabla(self):
        """Actualiza la tabla con los clientes"""
        self.tabla_clientes.rows.clear()
        
        clientes = self.banco.listar_clientes()
        
        if not clientes:
            # Mostrar mensaje si no hay clientes
            self.tabla_clientes.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("No hay clientes registrados", 
                                          italic=True, 
                                          color=ft.Colors.GREY_600,
                                          colspan=4))
                    ]
                )
            )
        else:
            for cliente in clientes:
                self.tabla_clientes.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(cliente.dni)),
                            ft.DataCell(ft.Text(cliente.nombre)),
                            ft.DataCell(ft.Text(cliente.apellido)),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.Icons.VISIBILITY,
                                    tooltip="Ver detalle",
                                    on_click=lambda e, d=cliente.dni: self.ver_detalle_cliente(d)
                                )
                            ),
                        ]
                    )
                )
    
    def render(self):
        """Renderiza la vista completa"""
        self.actualizar_tabla()
        
        return ft.Column(
            controls=[
                ft.Text("Gestión de Clientes", size=28, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                
                # Formulario para crear cliente
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Nuevo Cliente", size=18, weight=ft.FontWeight.BOLD),
                            ft.Row([
                                self.nombre_input,
                                self.apellido_input,
                                self.dni_input,
                                ft.ElevatedButton(
                                    "Agregar Cliente",
                                    icon=ft.Icons.PERSON_ADD,
                                    on_click=self.crear_cliente
                                ),
                            ], wrap=True),
                            self.mensaje,
                        ]),
                        padding=20,
                    ),
                    elevation=2,
                ),
                
                ft.Container(height=20),
                
                # Tabla de clientes
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Listado de Clientes", size=18, weight=ft.FontWeight.BOLD),
                            ft.Container(
                                content=self.tabla_clientes,
                                padding=10,
                            ),
                        ]),
                        padding=20,
                    ),
                    elevation=2,
                ),
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        )

