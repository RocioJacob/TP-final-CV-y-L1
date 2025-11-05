import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cuenta import CuentaAhorro, CuentaCorriente
from cliente import Cliente


class TestCuentaAhorro:
    """Tests para CuentaAhorro"""
    
    @pytest.fixture
    def cuenta(self):
        """Fixture que crea una cuenta de ahorro"""
        return CuentaAhorro(numero="001", titular_dni="12345678", tasa_interes=0.05)
    
    def test_crear_cuenta_ahorro(self, cuenta):
        """Prueba la creación de una cuenta de ahorro"""
        assert cuenta.numero == "001"
        assert cuenta.saldo == 0
        assert cuenta.tasa_interes == 0.05
    
    def test_ingresar_dinero(self, cuenta):
        """Prueba ingresar dinero"""
        cuenta.ingresar(1000)
        assert cuenta.saldo == 1000
    
    def test_retirar_dinero(self, cuenta):
        """Prueba retirar dinero"""
        cuenta.ingresar(1000)
        cuenta.retirar(300)
        assert cuenta.saldo == 700
    
    def test_retirar_sin_fondos(self, cuenta):
        """Prueba retirar sin fondos suficientes"""
        cuenta.ingresar(100)
        with pytest.raises(ValueError):
            cuenta.retirar(200)
    
    def test_calcular_interes(self, cuenta):
        """Prueba el cálculo de intereses"""
        cuenta.ingresar(1000)
        interes = cuenta.calcular_interes()
        assert interes == 50  # 1000 * 0.05
    
    def test_ingresar_monto_negativo(self, cuenta):
        """Prueba ingresar monto negativo"""
        with pytest.raises(ValueError):
            cuenta.ingresar(-100)


class TestCuentaCorriente:
    """Tests para CuentaCorriente"""
    
    @pytest.fixture
    def cuenta_corriente(self):
        """Fixture que crea una cuenta corriente"""
        return CuentaCorriente(
            numero="002",
            titular_dni="87654321",
            limite_descubierto=500
        )
    
    def test_crear_cuenta_corriente(self, cuenta_corriente):
        """Prueba la creación de una cuenta corriente"""
        assert cuenta_corriente.numero == "002"
        assert cuenta_corriente.limite_descubierto == 500
    
    def test_retirar_con_descubierto(self, cuenta_corriente):
        """Prueba retirar usando el descubierto"""
        cuenta_corriente.ingresar(100)
        cuenta_corriente.retirar(400)  # 100 + 300 de descubierto
        assert cuenta_corriente.saldo == -300
    
    def test_exceder_limite_descubierto(self, cuenta_corriente):
        """Prueba exceder el límite de descubierto"""
        with pytest.raises(ValueError):
            cuenta_corriente.retirar(600)


@pytest.mark.parametrize("monto,esperado", [
    (100, 100),
    (1000, 1000),
    (50.5, 50.5),
])
def test_ingresar_parametrizado(monto, esperado):
    """Test parametrizado para diferentes montos"""
    cuenta = CuentaAhorro("003", "11111111", 0.02)
    cuenta.ingresar(monto)
    assert cuenta.saldo == esperado