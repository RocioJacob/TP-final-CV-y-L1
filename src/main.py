import traceback
from almacenamiento import Banco
from interfaz_ui import run_flet_app
# Importamos CuentaAhorro para los datos de ejemplo
from cuenta import CuentaAhorro, CuentaCorriente 

# -------------------- SCRIPT PRINCIPAL --------------------

if __name__ == "__main__":
    banco = Banco()
    
    # Pre-cargar datos de ejemplo (opcional)
    try:
        c1 = banco.crear_cliente("Rocio", "Jacob", "12345678")
        ca = banco.crear_cuenta_ahorro(c1.dni, tasa_interes=0.02)
        ca.ingresar(1000)
        cc = banco.crear_cuenta_corriente(c1.dni, limite_descubierto=500.0)
        cc.ingresar(500)
    except Exception as e:
        # Se ignora si ya existe el cliente (debería ser la primera vez)
        print("Error pre-cargando datos de ejemplo (puede ser normal si ya existe):", e)
        pass

    # Ejecuta la app Flet si está disponible
    try:
        run_flet_app(banco)
    except ImportError as e:
        print("\n=======================================================")
        print("❌ Error: Módulo faltante para la Interfaz Gráfica.")
        print("Para ejecutar la UI instale **flet** (y opcionalmente **fpdf2** para el PDF).")
        print("Comandos recomendados:")
        print("pip install flet")
        print("pip install fpdf2")
        print("=======================================================\n")
    except Exception as e:
        print("Error lanzando la UI:", e)
        print(traceback.format_exc())