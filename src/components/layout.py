import flet as ft
import datetime
class BaseLayout:
    """Layout base con header y footer reutilizable"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        
    def create_header(self):
        """Header con título de la aplicación"""
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.ACCOUNT_BALANCE, color=ft.Colors.WHITE, size=30),
                    ft.Text(
                        "Sistema Bancario - TP Integrador Final",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.INDIGO_300,
            padding=20,
            width=float('inf')
        )
    
    def create_footer(self):
        """Footer con copyright"""
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(
                        f"© {datetime.datetime.now().year} Sistema Bancario - Laboratorio I  |  Desarrollado por: [Tu Nombre y el de tu compañera]",
                        size=12,
                        color=ft.Colors.WHITE70,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.INDIGO_300,
            padding=15,
            width=float('inf'),  # Ocupa todo el ancho disponible
        )
    
    def create_container(self, content):
        """Contenedor centrado como Bootstrap"""
        return ft.Container(
            content=content,
            padding=20,
            expand=True,
            alignment=ft.alignment.top_center,
        )
    
    def render(self, content):
        """Renderiza el layout completo"""
        return ft.Column(
            controls=[
                self.create_header(),
                self.create_container(content),
                self.create_footer(),
            ],
            spacing=0,
            expand=True,
        )