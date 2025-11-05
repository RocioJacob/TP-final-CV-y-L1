import flet as ft
from almacenamiento import Banco
from components.layout import BaseLayout
from views.cliente_list_view import ClienteListView
from views.cliente_detail_view import ClienteDetailView

def main(page: ft.Page):
    page.title = "Sistema Bancario - TP Integrador Final"
    page.padding = 0
    page.window_width = 1200
    page.window_height = 800
    
    # Inicializar banco
    banco = Banco()
    
    # Pre-cargar datos de ejemplo (opcional)
    try:
        c1 = banco.crear_cliente("Rocio", "Jacob", "12345678")
        ca = banco.crear_cuenta_ahorro(c1.dni, tasa_interes=0.02)
        ca.ingresar(1000)
        cc = banco.crear_cuenta_corriente(c1.dni, limite_descubierto=500.0)
        cc.ingresar(500)
        cc.retirar(200)
    except:
        pass
    
    # Layout base
    layout = BaseLayout(page)
    
    def navigate(vista: str, dni: str = None):
        """Navega entre vistas"""
        if vista == "listado":
            page.go("/")
        elif vista == "detalle" and dni:
            page.go(f"/detalle/{dni}")
    
    def route_change(route):
        """Maneja los cambios de ruta"""
        page.controls.clear()
        
        # Determinar qué vista mostrar
        if page.route == "/":
            # Vista listado de clientes
            vista = ClienteListView(page, banco, navigate)
            contenido = vista.render()
        elif page.route.startswith("/detalle/"):
            # Vista detalle de cliente
            dni = page.route.split("/")[-1]
            try:
                vista = ClienteDetailView(page, banco, dni, navigate)
                contenido = vista.render()
            except ValueError:
                contenido = ft.Text("Cliente no encontrado", size=24, color=ft.colors.RED_700)
        else:
            contenido = ft.Text("Página no encontrada", size=24)
        
        # Renderizar con el layout
        page.add(layout.render(contenido))
        page.update()
    
    # Configurar routing
    page.on_route_change = route_change
    page.go("/")

if __name__ == "__main__":
    # ft.app(target=main)
    ft.app(target=main, view=ft.WEB_BROWSER)
