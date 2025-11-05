import pytest
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cliente import Cliente


class TestCliente:
    """Tests para la clase Cliente"""
    
    def test_crear_cliente(self):
        """Prueba la creación de un cliente"""
        cliente = Cliente("Juan", "Pérez", "12345678")
        assert cliente.nombre == "Juan"
        assert cliente.apellido == "Pérez"
        assert cliente.dni == "12345678"
    
    def test_cliente_sin_cuentas(self):
        """Verifica que un cliente nuevo no tenga cuentas"""
        cliente = Cliente("María", "González", "87654321")
        assert len(cliente.cuentas) == 0
    
    def test_agregar_cuenta(self):
        """Prueba agregar una cuenta al cliente"""
        cliente = Cliente("Pedro", "Martínez", "11111111")
        # Aquí deberías importar la clase Cuenta y crear una
        # cuenta = CuentaAhorro(...)
        # cliente.agregar_cuenta(cuenta)
        # assert len(cliente.cuentas) == 1
    
    def test_dni_invalido(self):
        """Prueba validación de DNI"""
        with pytest.raises(ValueError):
            Cliente("Ana", "López", "")
    
    def test_nombre_vacio(self):
        """Prueba validación de nombre"""
        with pytest.raises(ValueError):
            Cliente("", "Rodríguez", "22222222")


class TestClienteIntegracion:
    """Tests de integración para Cliente"""
    
    @pytest.fixture
    def cliente_con_datos(self):
        """Fixture que crea un cliente de prueba"""
        return Cliente("Test", "Usuario", "99999999")
    
    def test_cliente_fixture(self, cliente_con_datos):
        """Prueba usando fixture"""
        assert cliente_con_datos.nombre == "Test"
        assert cliente_con_datos.dni == "99999999"