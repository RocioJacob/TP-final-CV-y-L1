import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from almacenamiento import Banco
from cliente import Cliente


class TestBanco:
    """Tests para la clase Banco"""
    
    @pytest.fixture
    def banco(self):
        """Fixture que crea un banco limpio"""
        return Banco()
    
    def test_crear_cliente(self, banco):
        """Prueba crear un cliente en el banco"""
        cliente = banco.crear_cliente("Carlos", "Gómez", "33333333")
        assert cliente.dni == "33333333"
        assert len(banco.clientes) == 1
    
    def test_buscar_cliente(self, banco):
        """Prueba buscar un cliente"""
        banco.crear_cliente("Laura", "Fernández", "44444444")
        cliente = banco.buscar_cliente("44444444")
        assert cliente is not None
        assert cliente.nombre == "Laura"
    
    def test_buscar_cliente_inexistente(self, banco):
        """Prueba buscar un cliente que no existe"""
        cliente = banco.buscar_cliente("99999999")
        assert cliente is None
    
    def test_crear_cuenta_ahorro(self, banco):
        """Prueba crear una cuenta de ahorro"""
        banco.crear_cliente("Pedro", "Silva", "55555555")
        cuenta = banco.crear_cuenta_ahorro("55555555", tasa_interes=0.03)
        assert cuenta.tasa_interes == 0.03
    
    def test_crear_cuenta_cliente_inexistente(self, banco):
        """Prueba crear cuenta para cliente inexistente"""
        with pytest.raises(ValueError):
            banco.crear_cuenta_ahorro("99999999")
    
    def test_listar_clientes(self, banco):
        """Prueba listar todos los clientes"""
        banco.crear_cliente("Ana", "Torres", "66666666")
        banco.crear_cliente("Luis", "Ramírez", "77777777")
        clientes = banco.listar_clientes()
        assert len(clientes) == 2