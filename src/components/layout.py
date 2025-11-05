import flet as ft

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
            bgcolor=ft.Colors.BLUE_700,
            padding=20,
        )
    
    def create_footer(self):
        """Footer con copyright"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "© 2024 Sistema Bancario - Laboratorio I",
                        size=12,
                        color=ft.Colors.WHITE70,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Desarrollado por: [Tu Nombre y el de tu compañera]",
                        size=11,
                        color=ft.Colors.WHITE60,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            bgcolor=ft.Colors.BLUE_900,
            padding=15,
        )
    
    def create_container(self, content):
        """Contenedor centrado como Bootstrap"""
        return ft.Container(
            content=content,
            padding=30,
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