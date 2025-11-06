import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cuenta import CuentaAhorro, CuentaCorriente
from cliente import Cliente

class TestCuentaAhorro:
    @pytest.fixture
    def cliente(self):
        return Cliente("Ana", "Perez", "12345678")

    @pytest.fixture
    def cuenta(self, cliente):
        return CuentaAhorro(cliente, tasa_interes=0.05)

    def test_crear_cuenta_ahorro(self, cuenta):
        assert hasattr(cuenta, "numero_cuenta")
        assert cuenta.saldo == 0.0

    def test_ingresar_y_retirar(self, cuenta):
        cuenta.ingresar(1000)
        assert cuenta.saldo == 1000.0
        cuenta.retirar(300)
        assert cuenta.saldo == 700.0

    def test_retirar_sin_fondos(self, cuenta):
        cuenta.ingresar(100)
        with pytest.raises(ValueError):
            cuenta.retirar(200)

    def test_aplicar_interes(self, cuenta):
        cuenta.ingresar(1000)
        cuenta.aplicar_interes()  # según la impl. aplica interés al saldo
        # 1000 + 1000*0.05 = 1050.0
        assert pytest.approx(cuenta.saldo, rel=1e-9) == 1050.0

    def test_ingresar_monto_negativo(self, cuenta):
        with pytest.raises(ValueError):
            cuenta.ingresar(-100)


class TestCuentaCorriente:
    @pytest.fixture
    def cliente(self):
        return Cliente("Juan", "Lopez", "87654321")

    @pytest.fixture
    def cc(self, cliente):
        return CuentaCorriente(cliente, limite_descubierto=500)

    def test_crear_cuenta_corriente(self, cc):
        assert hasattr(cc, "numero_cuenta")
        assert cc.saldo == 0.0

    def test_retirar_con_descubierto(self, cc):
        cc.ingresar(100)
        cc.retirar(400)  # debe permitir hasta 100 + 500 = 600
        assert cc.saldo == -300.0

    def test_exceder_limite_descubierto(self, cc):
        with pytest.raises(ValueError):
            cc.retirar(700)  # > 100 + 500 => error


@pytest.mark.parametrize("monto,esperado", [
    (100, 100.0),
    (1000, 1000.0),
    (50.5, 50.5),
])
def test_ingresar_parametrizado(monto, esperado):
    cliente = Cliente("X", "Y", "11111111")
    cuenta = CuentaAhorro(cliente, tasa_interes=0.02)
    cuenta.ingresar(monto)
    assert cuenta.saldo == esperado
